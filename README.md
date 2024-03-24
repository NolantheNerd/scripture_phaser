# Scripture Phaser

scripture_phaser helps you to memorize the Bible.

![scripture_phaser Demo](doc/demo.gif)

## Installation

This package is available through PIP:

pip install scripture_phaser

## Usage

scripture_phaser [-h] [--version] [--license]

Running scripture_phaser with no arguments launches the interactive CLI.

### Commands

scripture_phaser has a modal CLI. This means that the commands that are available to you vary depending on which mode you are in.

When you first start scripture_phaser, you are dropped into the standard mode (">" prompt) and have the following commands are available to you:

* l/list        - Lists selected reference, random single verse selection, translation, whether or not to show the passage numbers and whether or not fast recitation mode is selected
* n/numbers     - Toggles whether or not to include the passage numbers
* m/single      - Toggles whether or not to practice random single verses
* f/fast        - Toggles whether or not to use fast recitation mode when reciting
* r/reference   - Sets the reference
* t/translation - Set the translation
* i/inquire     - List available translations
* p/practice    - Practice the current reference
* v/view        - Preview current reference
* s/stats       - Enter statistics mode
* h/help        - Prints this help message
* q/quit        - Quits scripture_phaser

You can enter statistics mode by pressing "s" in standard mode ("\[STATS\] >" prompt). In statistics mode, the following commands are available to you:

* sd/start      - Sets the earliest date to use when fetching past recitation attempts
* ed/end        - Sets the latest date to use when fetching past recitation attempts
* l/list        - List current filters used in data selection (start/end date)
* c/clear       - Clears all current filters used in data selection (start/end date)
* a/all         - List all references ever attempted
* r/rank        - Rank all attempted verses by average recall accuracy
* d/delete      - Reset all statistics
* h/help        - Prints stats mode help message
* q/quit        - Return to the standard mode

You can enter fast recitation mode if you have fast recitations set to True and you press "p" to practice the passage (blank prompt). In fast recitation mode, the following commands are available to you:

* a-z A-Z 0-9   - Advances the recitation of the verse by one word
* ?             - Prints fast mode help message
* Ctrl + C      - Return to standard mode

## Uninstallation

pip uninstall scripture_phaser

## What's up with the Name?

Why is this tool called "scripture_phaser"? The name is actually a reference to a fictional weapon that appeared in an episode on of Focus on the Family's radio drama "Adventures in Odyssey" back in 1995 called "Hidden in My Heart".

In one particular segment of the show, the characters are parodying an away mission from the original "Star Trek" series with William Shatner. Sky Trip's own captain, played by William Shattered, along with his trusty sidekick Krok and one expendable crewman beam down to an alien world to rescue a damsel in distress. Among the other trinkets that they take with them are their scripture phasers. These devices thwart attempts to tempt the trio to sin by citing relevant pieces of scripture. The entire segment is very tongue-in-cheek, but absolutely entertaining.

The entire episode was released for free by Focus on the Family as a part of an episode of "The Official Adventures in Odyssey Podcast".

[Link to The Podcast Episode](https://www.oneplace.com/ministries/the-official-adventures-in-odyssey-podcast/player/june-13-2007-free-adventures-in-odyssey-episode-hidden-in-my-heart-798810.html)

The "Sky Trip" portion of the episode starts at 12:28, if you want to skip directly to it.

## License

scripture_phaser is licensed under the BSD 3-Clause License. See LICENSE file or the [Open Source Initiative](https://opensource.org/license/bsd-3-clause/) for the full text of the license.
