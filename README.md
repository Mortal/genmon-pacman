Display `pacman` upgrades with genmon
-------------------------------------

This is a Python 3 script to use with the
[Xfce4 Generic Monitor](http://goodies.xfce.org/projects/panel-plugins/xfce4-genmon-plugin)
in Arch Linux.

It runs `pacman -Sy` to update package lists in a temporary pacman db
and displays the number of packages to upgrade in the system tray.

Simply add a "Generic Monitor" to your Xfce panel.
Set the command to point to `genmon-pacman.py`
and set a suitable update period such as 1800 seconds (a half hour).

By Mathias Rav, March 2016.
