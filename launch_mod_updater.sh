#!/bin/bash

# Running 5 terminal instances
# You can edit it and add more or use less instances
# Adjust arguments values after the script's name

# Updating from the first mod to 37th
gnome-terminal -- bash -c "python rimworld_git_mods_installer_updater.py 0 37; exec bash"

# Updating more 37 mods = (0 + 37 = 37)
gnome-terminal -- bash -c "python rimworld_git_mods_installer_updater.py 37 37; exec bash"

# Updating more 36 mods = (37 + 36 = 74)
gnome-terminal -- bash -c "python rimworld_git_mods_installer_updater.py 74 36; exec bash"

# Updating more 36 mods = (74 + 36 = 110)
gnome-terminal -- bash -c "python rimworld_git_mods_installer_updater.py 110 36; exec bash"

# Updating last 37 mods = (110 + 37 = 146)
gnome-terminal -- bash -c "python rimworld_git_mods_installer_updater.py 146 37; exec bash"

# Total = 183 Mods! Yes, I have quite a bunch of mods installed... xD

# If you prefer xterm or another terminal, replace gnome-terminal with xterm -e