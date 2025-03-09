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

module Authentication exposing (..)

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

type alias UserCredentials =
  { name : String, username : String, email : String, token : String }

type alias SignInCredentials =
  { username : String, password : String }

type alias NewUserDetails =
  { name : String, username : String, password : String, email : String }

-- @@@ TODO: Change to UsernameTaken & EmailTaken with expectStringResponse
type UserError =
  None
  | InvalidCredentials
  | CredentialTaken

type User = 
  SignedInUser UserCredentials
  | SignedOutUser SignInCredentials
  | NewUser NewUserDetails

encode_login_credentials : SignInCredentials -> Encode.Value
encode_login_credentials credentials =
  Encode.object
    [ ("username", Encode.string credentials.username)
    , ("password", Encode.string credentials.password)
    ]

encode_signedin_user_credentials : UserCredentials -> Encode.Value
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

decode_signedin_user : Decode.Decoder UserCredentials
decode_signedin_user =
  Decode.map4 UserCredentials
    (Decode.field "name" Decode.string)
    (Decode.field "username" Decode.string)
    (Decode.field "email" Decode.string)
    (Decode.field "token" Decode.string)

type alias Model = 
  { user : User, user_error : UserError }

init : () -> (Model, Cmd Msg)
init () = (
  { user = NewUser { name = "", username = "", password = "", email = "" }
  , user_error = None }
  , Cmd.none
  )


-- Update

type Msg =
  NameInput String
  | UsernameInput String
  | EmailInput String
  | PasswordInput String
  | SignOut (Result Http.Error ())
  | SignInButtonClicked
  | SignIn (Result Http.Error UserCredentials)
  | SignOutButtonClicked
  | CreateUserButtonClicked

update_user : User -> Cmd Msg
update_user user =
  case user of
    -- Create User
    NewUser user_details ->
      Http.post
        { url = base_url ++ "/signup"
        , body = Http.jsonBody (encode_new_user_details user_details)
        , expect = Http.expectJson SignIn decode_signedin_user
        }

    -- Sign Out
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

    -- Sign In
    SignedOutUser user_credentials ->
      Http.post
        { url = base_url ++ "/login"
        , body = Http.jsonBody (encode_login_credentials user_credentials)
        , expect = Http.expectJson SignIn decode_signedin_user
        }

update : Msg -> Model -> (Model, Cmd Msg)
update msg model = 
  case msg of
    NameInput name ->
      case model.user of
        NewUser user_details ->
          ( { model | user = NewUser (NewUserDetails name user_details.username user_details.password user_details.email ) }, Cmd.none )

        SignedOutUser _ ->
          ( model, Cmd.none )

        SignedInUser _ ->
          ( model, Cmd.none )

    UsernameInput username ->
      case model.user of
        NewUser user_details ->
          ( { model | user = NewUser (NewUserDetails user_details.name username user_details.password user_details.email ) }, Cmd.none )

        SignedOutUser user_credentials ->
          ( { model | user = SignedOutUser (SignInCredentials username user_credentials.password) }, Cmd.none )

        SignedInUser _ ->
          ( model, Cmd.none )

    PasswordInput password ->
      case model.user of
        NewUser user_details ->
          ( { model | user = NewUser (NewUserDetails user_details.name user_details.username password user_details.email ) }, Cmd.none )

        SignedOutUser user_credentials ->
          ( { model | user = SignedOutUser (SignInCredentials user_credentials.username password) }, Cmd.none )

        SignedInUser _ ->
          ( model, Cmd.none )

    EmailInput email ->
      case model.user of
        NewUser user_details ->
          ( { model | user = NewUser (NewUserDetails user_details.name user_details.username user_details.password email ) }, Cmd.none )

        SignedOutUser _ ->
          ( model, Cmd.none )

        SignedInUser _ ->
          ( model, Cmd.none )

    SignOutButtonClicked ->
      ( model, update_user model.user )

    SignOut _ ->
      ( { model | user = SignedOutUser (SignInCredentials "" "") }, Cmd.none )

    SignInButtonClicked ->
      case model.user of
        NewUser _ ->
          ( { model | user = SignedOutUser (SignInCredentials "" ""), user_error = None }, Cmd.none )

        SignedOutUser _ ->
          ( model, update_user model.user )

        SignedInUser _ ->
          ( model, Cmd.none )

    SignIn result ->
      case result of
        Ok user_credentials ->
          ( { model | user = SignedInUser user_credentials, user_error = None}, Cmd.none )

        Err error ->
          case model.user of
            NewUser user_details ->
              case error of
                Http.BadStatus _ ->
                  ( { model | user = NewUser (NewUserDetails "" "" "" ""), user_error = CredentialTaken }, Cmd.none )
                Http.BadUrl _ ->
                  ( model , Cmd.none )
                Http.Timeout ->
                  ( model , Cmd.none )
                Http.NetworkError ->
                  ( model , Cmd.none )
                Http.BadBody _ ->
                  ( model , Cmd.none )

            SignedInUser _ ->
              ( model, Cmd.none )

            SignedOutUser _ ->
              case error of
                Http.BadStatus _ ->
                  ( { model | user = SignedOutUser (SignInCredentials "" ""), user_error = InvalidCredentials }, Cmd.none )
                Http.BadUrl _ ->
                  ( model , Cmd.none )
                Http.Timeout ->
                  ( model , Cmd.none )
                Http.NetworkError ->
                  ( model , Cmd.none )
                Http.BadBody _ ->
                  ( model , Cmd.none )

    CreateUserButtonClicked ->
      case model.user of
        NewUser _ ->
          ( model, update_user model.user )

        SignedOutUser _ ->
          ( { model | user = NewUser (NewUserDetails "" "" "" ""), user_error = None }, Cmd.none )

        SignedInUser _ ->
          ( model, Cmd.none )


-- View

type alias Document msg =
  { title : String
  , body : List (Html.Html msg)
  }

view : Model -> Document Msg
view model =
  case model.user of
    NewUser user_details ->
      case model.user_error of
        None ->
          { title = "Create Account"
          , body =
            [ Html.div [] [
              Html.p [] [ Html.text "Create Account" ]
            , Html.p [] [ Html.text "Name" ]
            , Html.input [ Attributes.type_ "text", Attributes.placeholder "John Doe", Attributes.value user_details.name, Events.onInput NameInput ] []
            , Html.p [] [ Html.text "Username" ]
            , Html.input [ Attributes.type_ "text", Attributes.placeholder "jdoe", Attributes.value user_details.username, Events.onInput UsernameInput ] []
            , Html.p [] [ Html.text "Email Address" ]
            , Html.input [ Attributes.type_ "text", Attributes.placeholder "john.doe@example.com", Attributes.value user_details.email, Events.onInput EmailInput ] []
            , Html.p [] [ Html.text "Password" ]
            , Html.input [ Attributes.type_ "password", Attributes.placeholder "password123", Attributes.value user_details.password, Events.onInput PasswordInput ] []
            , Html.button [ Events.onClick CreateUserButtonClicked ] [ Html.text "Create" ]
            , Html.button [ Events.onClick SignInButtonClicked ] [ Html.text "Sign In" ]
            ] ]
          }

        CredentialTaken ->
          { title = "Create Account"
          , body =
            [ Html.div [] [
              Html.p [] [ Html.text "Create Account" ]
            , Html.p [] [ Html.text "Name" ]
            , Html.input [ Attributes.type_ "text", Attributes.placeholder "John Doe", Attributes.value user_details.name, Events.onInput NameInput ] []
            , Html.p [] [ Html.text "Username" ]
            , Html.input [ Attributes.type_ "text", Attributes.placeholder "jdoe", Attributes.value user_details.username, Events.onInput UsernameInput ] []
            , Html.p [] [ Html.text "Email Address" ]
            , Html.input [ Attributes.type_ "text", Attributes.placeholder "john.doe@example.com", Attributes.value user_details.email, Events.onInput EmailInput ] []
            , Html.p [] [ Html.text "Password" ]
            , Html.input [ Attributes.type_ "password", Attributes.placeholder "password123", Attributes.value user_details.password, Events.onInput PasswordInput ] []
            , Html.p [] [ Html.text "Sorry! Username or Email Already Taken!" ]
            , Html.button [ Events.onClick CreateUserButtonClicked ] [ Html.text "Create" ]
            , Html.button [ Events.onClick SignInButtonClicked ] [ Html.text "Sign In" ]
            ] ]
          }

        InvalidCredentials ->
          { title = "Whoops!"
          , body =
            [ Html.div [] [
              Html.p [] [ Html.text "Whoops! You shouldn't be able to get to this page!" ]
            ] ]
          }

    SignedOutUser user_credentials ->
      case model.user_error of
        None ->
          { title = "Scripture Phaser"
          , body =
              [ Html.div [] [
                Html.p [] [ Html.text "Welcome to Scripture Phaser!"]
              , Html.p [] [ Html.text "Username"]
              , Html.input [ Attributes.type_ "text", Attributes.placeholder "Username", Attributes.value user_credentials.username, Events.onInput UsernameInput ] []
              , Html.p [] [ Html.text "Password"]
              , Html.input [ Attributes.type_ "password", Attributes.placeholder "Password", Attributes.value user_credentials.password, Events.onInput PasswordInput ] []
              , Html.button [ Events.onClick SignInButtonClicked ] [ Html.text "Sign In" ]
              , Html.button [ Events.onClick CreateUserButtonClicked ] [ Html.text "Create" ]
              ] ]
          }

        CredentialTaken ->
          { title = "Whoops!"
          , body =
            [ Html.div [] [
              Html.p [] [ Html.text "Whoops! You shouldn't be able to get to this page!" ]
            ] ]
          }

        InvalidCredentials ->
          { title = "Scripture Phaser"
          , body =
              [ Html.div [] [
                Html.p [] [ Html.text "Welcome to Scripture Phaser!"]
              , Html.p [] [ Html.text "Username"]
              , Html.input [ Attributes.type_ "text", Attributes.placeholder "Username", Attributes.value user_credentials.username, Events.onInput UsernameInput ] []
              , Html.p [] [ Html.text "Password"]
              , Html.input [ Attributes.type_ "password", Attributes.placeholder "Password", Attributes.value user_credentials.password, Events.onInput PasswordInput ] []
              , Html.p [] [ Html.text "Sorry! Wrong username or password." ]
              , Html.button [ Events.onClick SignInButtonClicked ] [ Html.text "Sign In" ]
              , Html.button [ Events.onClick CreateUserButtonClicked ] [ Html.text "Create" ]
              ] ]
          }

    SignedInUser signedin_user_credentials ->
      { title = "Welcome!"
      , body =
          [ Html.div [] [
            Html.p [] [ Html.text ("Welcome " ++ signedin_user_credentials.name) ]
          , Html.button [ Events.onClick SignOutButtonClicked ] [ Html.text "Sign Out" ]
          ] ]
      }


-- Subscription

subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none


-- Main

main = Browser.document { init = init, update = update, view = view, subscriptions = subscriptions }
