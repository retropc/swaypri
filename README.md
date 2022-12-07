# swaypri

## Description

Prioritises application that is focused (Windows style...)

Useful on ancient laptops!

Supports sway only (previously supported X).

## Setup

Configure PAM to allow your user to increase priority beyond the default by adding the following line to ```/etc/security/limits.d/blah.conf```:

```
youruser   -    nice   -20
```

Log out and in again.

If you need to set priorities for other users (e.g. qemu/libvirt), compile "nicer" and give it that capability:

```
gcc -o nicer nicer.c -Wall -Werror -pedantic -std=c99
chmod 700 nicer
sudo setcap CAP_SYS_NICE+ep nicer
```

Copy config.py.example to config.py and adjust as necessary.

A systemd unit is also included (but will need editing also).
