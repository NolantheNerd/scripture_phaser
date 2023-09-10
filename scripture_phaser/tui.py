# scripture_phaser helps you to memorize the Word of Truth.
# Copyright (C) 2023 Nolan McMahon
#
# This file is part of scripture_phaser.
#
# scripture_phaser is licensed under the terms of the BSD 3-Clause License
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import pytermgui as ptg
from scripture_phaser.api import API

class TUI:
    def __init__(self):
        self.api = API()

        window = ptg.window_manager.Window(
            title="Scripture Phaser",
            is_noresize=True,
            is_static=True,
            allow_fullscreen=True
        ).center()

        info_cont = ptg.Container()

        mode_button = ptg.Button(
            f"Random Mode: {self._get_mode_label(self.api.mode)}",
            self._update_mode
        )
        trans_button = ptg.Button(
            f"Translation: {self.api.translation}",
            self._update_translation
        )

        info_cont.set_widgets([mode_button])
        window.set_widgets([info_cont])

        with ptg.WindowManager() as manager:
            manager.add(window)

    def _update_mode(self, mode_button):
        new_mode = not self.api.mode
        self.api.mode = new_mode
        mode_button.label = f"Random Mode: {self._get_mode_label(new_mode)}"

    def _get_mode_label(self, mode):
        if mode:
            return "On"
        return "Off"

    def _update_translation(self, translation_button):
        translation_window = ptg.window_manager.Window(
            title="Choose Translation",
            is_noresize=True,
            is_statis=True,
            allow_fullscreen=True
        ).center()

        translation_cont = ptg.Container()

        with ptg.WindowManager() as manager:
            manager.add(translation_window)

if __name__ == "__main__":
    tui = TUI()
