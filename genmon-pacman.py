#!/usr/bin/env python3

import argparse
import textwrap
import subprocess


def test():
    """
    >>> test()  # doctest:+ELLIPSIS
    <txt>105</txt>
    <tool>Need to upgrade 105 packages; 59.8 MB to download.
    <BLANKLINE>
    accountsservice, ..., xkeyboard-config</tool>
    """

    pkgs = """
        openssl libldap krb5 accountsservice apr-util apache avahi binutils
        gnutls libdatrie libthai gtk2 libssh2 curl libetpan sqlite claws-mail
        cups-pk-helper xkeyboard-config efl efl-docs freerdp python2
        libmariadbclient postgresql-libs gdal gegl02 geoclue2 git
        libimobiledevice mutter wpa_supplicant gnome-shell neon rtmpdump
        gst-plugins-bad gstreamer0.10-bad gstreamer0.10-bad-plugins irssi ldns
        lib32-openssl lib32-libssh2 lib32-libldap lib32-krb5 lib32-curl qt4
        lib32-qt4 libevent libgit2 libpagemaker libshout lighttpd lynx
        mariadb-clients mariadb mutt nmap nodejs openvpn php php-apache
        postgresql ptlib pypy3 python python-dbus-common python-dbus
        python2-dbus python2-eyed3 qca-qt4 qt5-base qt5-xmlpatterns
        qt5-declarative qt5-connectivity qt5-enginio qt5-graphicaleffects
        qt5-imageformats qt5-location qt5-multimedia qt5-sensors qt5-webchannel
        qt5-webkit qt5-script qt5-quick1 qt5-quickcontrols qt5-serialport
        qt5-svg qt5-translations qt5-tools qt5-websockets qt5-x11extras
        rdesktop redland redland-storage-virtuoso ruby s-nail serf sg3_utils
        spice-gtk3 squid syslog-ng transmission-cli transmission-qt unbound
        wget""".split()
    sizes = [0] * len(pkgs)
    sizes[0] = 59.8 * 1024**2
    print_status(list(zip(pkgs, sizes)))


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    subprocess.call(
        ('sudo', '-n', 'pacman', '-Sy'),
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    output = subprocess.check_output(
        ('pacman', '-Sup', '--print-format', 'PKG %n %s'),
        universal_newlines=True)

    pkgs = []
    for line in output.splitlines():
        if line.startswith("PKG "):
            name, size = line.split()[1:]
            pkgs.append((name, int(size)))
    print_status(pkgs)


def print_status(pkgs):
    print("<txt>%d</txt>" % len(pkgs))
    pkgs_str = textwrap.wrap(', '.join(sorted(n for n, s in pkgs)),
                             break_on_hyphens=False, width=55)
    print("<tool>Need to upgrade %d packages; " % len(pkgs) +
          "%.1f MB to download.\n\n" % (sum(s for n, s in pkgs) / 1024**2) +
          "%s</tool>" % '\n'.join(pkgs_str))


if __name__ == "__main__":
    main()
