#!/usr/bin/env python3

import os
import shlex
import argparse
import datetime
import textwrap
import itertools
import subprocess


def test():
    """
    >>> test()  # doctest:+ELLIPSIS
    <txt>105</txt>
    <tool>Need to upgrade 105 packages; 59.8 MB to download.
    <BLANKLINE>
    accountsservice, ...xkeyboard-config</tool>
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
    parser.add_argument('-n', '--no-update',
                        dest='update', action='store_false')
    parser.add_argument('-l', '--max-lines', type=int, default=None)
    parser.add_argument('-w', '--width', type=int, default=59)
    parser.add_argument('--terminal',
                        dest='terminal', default='gnome-terminal')
    parser.add_argument('--no-terminal',
                        dest='terminal', action='store_const', const=None)
    parser.add_argument('--icons',
                        default='/usr/share/icons/gnome/24x24/status')
    parser.add_argument('--icon',
                        default='software-update-available.png')
    args = parser.parse_args()

    d = '/tmp/checkup-db/'
    lock = d + 'db.lck'
    try:
        if not os.path.exists(d):
            os.mkdir(d)
            os.symlink('/var/lib/pacman/local', d + 'local')
        if args.update:
            subprocess.call(
                ('fakeroot', '--', 'pacman', '-Sy',
                 '--dbpath', d, '--logfile', '/dev/null'),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
        else:
            subprocess.call(
                ('rsync', '-aqu', '/var/lib/pacman/sync/', d + 'sync/'))
        output = subprocess.check_output(
            ('pacman', '-Sup', '--print-format', 'PKG %n %s',
             '--dbpath', d, '--logfile', '/dev/null'),
            universal_newlines=True)
    finally:
        try:
            os.unlink(lock)
        except:
            pass

    pkgs = []
    for line in output.splitlines():
        if line.startswith("PKG "):
            name, size = line.split()[1:]
            pkgs.append((name, int(size)))
    print_status(pkgs, max_lines=args.max_lines, width=args.width)
    if args.terminal is not None and pkgs:
        print("<img>%s/%s</img>" %
              (args.icons, args.icon))
        print("<click>%s -e %s</click>" %
              (shlex.quote(args.terminal),
               shlex.quote('sudo pacman -Syu')))



def join_prefixes(names):
    def get_prefix(n):
        try:
            return n[:n.index('-')+1]
        except ValueError:
            if n.startswith('lib'):
                return 'lib'
            return n

    groups = itertools.groupby(sorted(names, key=get_prefix), key=get_prefix)

    for prefix, group in groups:
        group = sorted(group)
        if len(group) > 1:
            group = [n[len(prefix):] for n in group]
            group[0] = '%s{%s' % (prefix, group[0])
            group[-1] += '}'
            yield from group
        else:
            yield from group


def print_status(pkgs, max_lines=None, width=59):
    print("<txt>%d</txt>" % len(pkgs))
    if not pkgs:
        dt = datetime.datetime.now()
        dt = dt.strftime("%Y-%m-%d %H:%M")
        print("<tool>No updates available\nLast checked on %s</tool>" % dt)
        return
    names = join_prefixes(n for n, s in pkgs)
    pkgs_str = textwrap.wrap(', '.join(names),
                             break_on_hyphens=False, width=width)
    if max_lines is not None and len(pkgs_str) + 2 > max_lines:
        pkgs_str = pkgs_str[:max_lines - 2]
        pkgs_str[-1] += ' ...'
    print("<tool>Need to upgrade %d packages; " % len(pkgs) +
          "%.1f MB to download.\n\n" % (sum(s for n, s in pkgs) / 1024**2) +
          "%s</tool>" % '\n'.join(pkgs_str))


if __name__ == "__main__":
    main()
