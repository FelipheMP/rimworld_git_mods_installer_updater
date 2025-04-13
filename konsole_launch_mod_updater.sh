#!/bin/bash

# Running 5 terminal instances in parallel
# Adjust arguments values after the script's name

# Updating from the first mod to 37th
konsole -e python rimworld_git_mods_installer_updater.py 0 37 &

# Updating more 37 mods = (0 + 37 = 37)
konsole -e python rimworld_git_mods_installer_updater.py 37 37 &

# Updating more 36 mods = (37 + 36 = 74)
konsole -e python rimworld_git_mods_installer_updater.py 74 36 &

# Updating more 36 mods = (74 + 36 = 110)
konsole -e python rimworld_git_mods_installer_updater.py 110 36 &

# Updating last 37 mods = (110 + 37 = 146)
konsole -e python rimworld_git_mods_installer_updater.py 146 37 &

# Total = 183 Mods! Yes, I have quite a bunch of mods installed... xD
