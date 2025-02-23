{-
   scripture_phaser helps you to memorize the Bible.
   Copyright (C) 2023-2025 Nolan McMahon
   
   This file is part of scripture_phaser.
   
   scripture_phaser is licensed under the terms of the BSD 3-Clause License
   
   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are met:
   
   1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
   
   2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
   
   3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software without
   specific prior written permission.
   
   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
   POSSIBILITY OF SUCH DAMAGE.
-}

module Main exposing (..)

import Http
import Browser
import Html
import Html.Attributes as Attributes
import Html.Events as Events
import Json.Encode as Encode
import Json.Decode as Decode


base_url : String
base_url = "http://localhost:8000"


-- Model

type alias SignedInUserCredentials =
  { name : String, username : String, email : String, token : String }

type alias LoginCredentials =
  { username : String, password : String }

type alias NewUserDetails =
  { name : String, username : String, password : String, email : String }

type User = 
  SignedInUser SignedInUserCredentials
  | SignedOutUser LoginCredentials
  | NewUser NewUserDetails

encode_login_credentials : LoginCredentials -> Encode.Value
encode_login_credentials credentials =
  Encode.object
    [ ("username", Encode.string credentials.username)
    , ("password", Encode.string credentials.password)
    ]

encode_signedin_user_credentials : SignedInUserCredentials -> Encode.Value
encode_signedin_user_credentials credentials =
  Encode.object
    [ ("name", Encode.string credentials.name)
    , ("username", Encode.string credentials.username)
    , ("email", Encode.string credentials.email)
    , ("token", Encode.string credentials.token)
    ]

encode_new_user_details : NewUserDetails -> Encode.Value
encode_new_user_details details =
  Encode.object
    [ ("name", Encode.string details.name)
    , ("username", Encode.string details.username)
    , ("email", Encode.string details.email)
    , ("password", Encode.string details.password)
    ]

decode_signedin_user : Decode.Decoder SignedInUserCredentials
decode_signedin_user =
  Decode.map4 SignedInUserCredentials
    (Decode.field "name" Decode.string)
    (Decode.field "username" Decode.string)
    (Decode.field "email" Decode.string)
    (Decode.field "token" Decode.string)

type alias Model = 
  { user : User }

init : () -> (Model, Cmd Msg)
init () = (
  { user = NewUser { name = "", username = "", password = "", email = "" } }
  , Cmd.none
  )


-- Update

type Msg =
  Name String
  | Username String
  | Email String
  | Password String
  | SignOut (Result Http.Error ())
  | SignInRequest
  | GotSignedInUser (Result Http.Error SignedInUserCredentials)
  | SignOutRequest
  | CreateUserRequest

createuser : User -> Cmd Msg
createuser user =
  case user of
    NewUser user_details ->
      Http.post
        { url = base_url ++ "/signup"
        , body = Http.jsonBody (encode_new_user_details user_details)
        , expect = Http.expectJson GotSignedInUser decode_signedin_user
        }

    SignedInUser _ ->
      Cmd.none

    SignedOutUser _ ->
      Cmd.none

signin : User -> Cmd Msg
signin user =
  case user of
    NewUser _ ->
      Cmd.none

    SignedInUser _ ->
      Cmd.none

    SignedOutUser user_credentials ->
      Http.post
        { url = base_url ++ "/login"
        , body = Http.jsonBody (encode_login_credentials user_credentials)
        , expect = Http.expectJson GotSignedInUser decode_signedin_user
        }

signout : User -> Cmd Msg
signout user =
  case user of
    NewUser _ ->
      Cmd.none

    SignedInUser signedin_user_credentials ->
      Http.request
        { method = "DELETE"
        , headers = []
        , url = base_url ++ "/logout"
        , body = Http.jsonBody (encode_signedin_user_credentials signedin_user_credentials)
        , expect = Http.expectWhatever SignOut
        , timeout = Nothing
        , tracker = Nothing
        }

    SignedOutUser _ ->
      Cmd.none

update : Msg -> Model -> (Model, Cmd Msg)
update msg model = 
  case msg of
    Name name ->
      case model.user of
        NewUser user_details ->
          ( { model | user = NewUser (NewUserDetails name user_details.username user_details.password user_details.email ) }, Cmd.none )

        SignedOutUser _ ->
          ( model, Cmd.none )

        SignedInUser _ ->
          ( model, Cmd.none )

    Username username ->
      case model.user of
        NewUser user_details ->
          ( { model | user = NewUser (NewUserDetails user_details.name username user_details.password user_details.email ) }, Cmd.none )

        SignedOutUser user_credentials ->
          ( { model | user = SignedOutUser (LoginCredentials username user_credentials.password) }, Cmd.none )

        SignedInUser _ ->
          ( model, Cmd.none )

    Password password ->
      case model.user of
        NewUser user_details ->
          ( { model | user = NewUser (NewUserDetails user_details.name user_details.username password user_details.email ) }, Cmd.none )

        SignedOutUser user_credentials ->
          ( { model | user = SignedOutUser (LoginCredentials user_credentials.username password) }, Cmd.none )

        SignedInUser _ ->
          ( model, Cmd.none )

    Email email ->
      case model.user of
        NewUser user_details ->
          ( { model | user = NewUser (NewUserDetails user_details.name user_details.username user_details.password email ) }, Cmd.none )

        SignedOutUser _ ->
          ( model, Cmd.none )

        SignedInUser _ ->
          ( model, Cmd.none )

    SignOutRequest ->
      ( model, signout model.user )

    SignOut _ ->
      ( { model | user = SignedOutUser (LoginCredentials "" "") }, Cmd.none )

    SignInRequest ->
      ( model, signin model.user )

    GotSignedInUser result ->
      case result of
        Ok user_credentials ->
          ( { model | user = SignedInUser user_credentials }, Cmd.none )

        Err error ->
          ( model , Cmd.none )

    CreateUserRequest ->
      ( model, createuser model.user )


-- View

type alias Document msg =
  { title : String
  , body : List (Html.Html msg)
  }

view : Model -> Document Msg
view model =
  case model.user of
    NewUser user_details ->
      { title = "Create Account"
      , body =
        [ Html.div [] [
          Html.p [] [ Html.text "Create Account" ]
        , Html.p [] [ Html.text "Name" ]
        , Html.input [ Attributes.type_ "text", Attributes.placeholder "John Doe", Attributes.value user_details.name, Events.onInput Name ] []
        , Html.p [] [ Html.text "Username" ]
        , Html.input [ Attributes.type_ "text", Attributes.placeholder "jdoe", Attributes.value user_details.username, Events.onInput Username] []
        , Html.p [] [ Html.text "Email Address" ]
        , Html.input [ Attributes.type_ "text", Attributes.placeholder "john.doe@example.com", Attributes.value user_details.email, Events.onInput Email ] []
        , Html.p [] [ Html.text "Password" ]
        , Html.input [ Attributes.type_ "password", Attributes.placeholder "password123", Attributes.value user_details.password, Events.onInput Password ] []
        , Html.button [ Events.onClick CreateUserRequest ] [ Html.text "Create" ]
        ] ]
      }

    SignedOutUser user_credentials ->
      { title = "SignedOutUser Title"
      , body =
          [ Html.div [] [
            Html.p [] [ Html.text "Welcome to Scripture Phaser!"]
          , Html.p [] [ Html.text "Username"]
          , Html.input [ Attributes.type_ "text", Attributes.placeholder "Username", Attributes.value user_credentials.username, Events.onInput Username ] []
          , Html.p [] [ Html.text "Password"]
          , Html.input [ Attributes.type_ "password", Attributes.placeholder "Password", Attributes.value user_credentials.password, Events.onInput Password ] []
          , Html.button [Events.onClick SignInRequest] [ Html.text "Sign In"]
          ] ]
      }

    SignedInUser signedin_user_credentials ->
      { title = "SignedIn Title"
      , body =
          [ Html.div [] [
            Html.p [] [ Html.text ("Welcome " ++ signedin_user_credentials.name)]
          , Html.button [Events.onClick SignOutRequest] [ Html.text "Sign Out"]
          ] ]
      }


-- Subscription

subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none


-- Main

main = Browser.document { init = init, update = update, view = view, subscriptions = subscriptions }
