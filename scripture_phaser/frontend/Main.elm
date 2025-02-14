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
import Html.Events exposing (onClick)


-- Model

type User = 
  SignedInUser { name : String, username : String, email : String, usertoken : String}
  | Guest

type alias Model = {
    user : User
  }

init : () -> (Model, Cmd Msg)
init = (
  { user = Guest }
  , Cmd.none
  )


-- Update

type Msg = SignIn | SignOut

update : Msg -> Model -> (Model, Cmd Msg)
update msg model = 
  case msg of
    SignOut ->
      ( { model | user = Guest }, Cmd.none )

    SignIn ->
      ( { model | user = SignedInUser { name = "Joe", username = "jsmith", email = "j@example.com", usertoken = "1234" } }, Cmd.none )


-- View

view : Model -> Html Msg
view model =
  case model.user of
    Guest ->
      div [] [
      p [] [text "Welcome to Scripture Phaser!"],
      p [] [text "Username"],
      input [] [],
      p [] [text "Password"],
      input [] [],
      button [onClick SignIn] [text "Sign In"]
      ]

    SignedInUser { name, username, email, usertoken } ->
      div [] [
      p [] [text ("Welcome " ++ name)],
      button [onClick SignOut] [text "Sign Out"]
      ]

-- Subscription

subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none

-- Main

main = Browser.element { init = init, update = update, view = view, subscriptions = subscriptions }
