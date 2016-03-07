Display `pacman` upgrades with genmon
-------------------------------------

This is a Python 3 script to use with the
[Xfce4 Generic Monitor](http://goodies.xfce.org/projects/panel-plugins/xfce4-genmon-plugin)
in Arch Linux.

It runs `pacman -Sy` to update package lists
and displays the number of packages to upgrade in the system tray.

To use it, make sure you can run `pacman -Sy` with sudo without a password prompt
by adding a line like the following to `/etc/sudoers`:

```
%wheel ALL=(root) NOPASSWD: /usr/bin/pacman -Sy
```

Be sure to always edit `/etc/sudoers` with `sudo visudo` to prevent syntax
errors from messing up your ability to run sudo!

Then simply add a "Generic Monitor" to your Xfce panel.
Set the command to point to `genmon-pacman.py`
and set a suitable update period such as 1800 seconds (a half hour).

By Mathias Rav, March 2016.
