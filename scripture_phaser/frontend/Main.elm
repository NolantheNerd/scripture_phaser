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

import Browser
import Html exposing (Html, div, p, text, button, input)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick, onInput)
import Json.Encode as Encode
import Json.Decode as Decode
import Http
import Debug


base_url : String
base_url = "http://localhost:8000"


-- Model

type alias SignedInUserCredentials =
  { name : String, username : String, email : String, usertoken : String }

type User = 
  SignedInUser SignedInUserCredentials
  | Guest UserCredentials

type alias UserCredentials =
  { username : String, password : String }

encode_user_credentials : UserCredentials -> Encode.Value
encode_user_credentials credentials =
  Encode.object
    [ ("username", Encode.string credentials.username)
    , ("password", Encode.string credentials.password)
    ]

decode_signedin_user : Decode.Decoder SignedInUserCredentials
decode_signedin_user =
  Decode.map4 SignedInUserCredentials
    (Decode.field "name" Decode.string)
    (Decode.field "username" Decode.string)
    (Decode.field "email" Decode.string)
    (Decode.field "usertoken" Decode.string)

type alias Model = 
  { user : User }

init : () -> (Model, Cmd Msg)
init () = (
  { user = Guest { username = "", password = "" } }
  , Cmd.none
  )


-- Update

type Msg = Username String | Password String | SignOut | SignIn | GotSignedInUser (Result Http.Error SignedInUserCredentials)

signin : User -> Cmd Msg
signin user =
  case user of
    SignedInUser signedin_user_credentials ->
      Cmd.none

    Guest user_credentials ->
      Http.post
        { url = base_url ++ "/login"
        , body = Http.jsonBody (encode_user_credentials user_credentials)
        , expect = Http.expectJson GotSignedInUser decode_signedin_user
        }

update : Msg -> Model -> (Model, Cmd Msg)
update msg model = 
  case msg of
    Username username ->
      case model.user of
        Guest user_credentials ->
          ( { model | user = Guest (UserCredentials username user_credentials.password) }, Cmd.none )

        SignedInUser _ ->
          ( model, Cmd.none )

    Password password ->
      case model.user of
        Guest user_credentials ->
          ( { model | user = Guest (UserCredentials user_credentials.username password) }, Cmd.none )

        SignedInUser _ ->
          ( model, Cmd.none )

    SignOut ->
      ( model, Cmd.none )

    SignIn ->
      ( model, signin model.user )

    GotSignedInUser result ->
      case result of
        Ok user_credentials ->
          ( { model | user = SignedInUser user_credentials }, Cmd.none )

        Err _ ->
          ( model , Cmd.none )


-- View

type alias Document msg =
  { title : String
  , body : List (Html msg)
  }

view : Model -> Document Msg
view model =
  case model.user of
    Guest user_credentials ->
      { title = "Guest Title"
      , body =
          [ div [] [
          p [] [text "Welcome to Scripture Phaser!"],
          p [] [text "Username"],
          input [ type_ "text", placeholder "Username", value user_credentials.username, onInput Username ] [],
          p [] [text "Password"],
          input [ type_ "password", placeholder "Password", value user_credentials.password, onInput Password ] [],
          button [onClick SignIn] [text "Sign In"]
          ] ]
      }

    SignedInUser { name, username, email, usertoken } ->
      { title = "SignedIn Title"
      , body =
          [ div [] [
          p [] [text ("Welcome " ++ name)],
          button [onClick SignOut] [text "Sign Out"]
          ] ]
      }

-- Subscription

subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none

-- Main

main = Browser.document { init = init, update = update, view = view, subscriptions = subscriptions }
