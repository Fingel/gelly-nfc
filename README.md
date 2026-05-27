# Gelly-NFC

https://github.com/user-attachments/assets/8489853c-48c8-4f45-a402-adfe440c6483

A script to control [the Gelly Jellyfin/Subsonic client](https://github.com/Fingel/gelly) via a NFC card reader. Make a jukebox!

The script can be adapted to work for any player - it just parses card text and runs arbitrary commands. 

[Read this post](https://www.pedaldrivenprogramming.com/2026/05/self-hosted-jukebox-with-nfc-cards/) that goes into further detail.

## Usage

Write some text to a blank card:
```bash
uv run main.py write "album:a7eaa2055a9aed8141e22377d467cb1e"
```

Listen for card taps and control Gelly:

```bash
$ uv run main.py
Watching for NFC tags... (Ctrl-C to stop)
Running: ['flatpak', 'run', 'io.m51.Gelly', '--big-player', '--play-album', 'a7eaa2055a9aed8141e22377d467cb1e']
```

## Likely required system packages

Arch:   ccid acsccid pcsclite pcsc-tools

Debian: libccid libacsccid1 pcscd pcsc-tools

## Misc
[pcsc_ndef.py](pcsc_ndef.py) taken from [github.com/Giraut/pcsc-ndef](https://github.com/Giraut/pcsc-ndef)
