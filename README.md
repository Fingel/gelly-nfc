# Gelly-NFC

https://github.com/user-attachments/assets/8489853c-48c8-4f45-a402-adfe440c6483

A script to control [the Gelly Jellyfin/Subsonic client](https://github.com/Fingel/gelly) via a NFC card reader. Make a jukebox!

The script can be adapted to work for any player - it just parses card text and runs arbitrary commands. 

[Read this post](https://www.pedaldrivenprogramming.com/2026/05/self-hosted-jukebox-with-nfc-cards/) that goes into further detail.

## Usage
I highly recommend installing and using [uv](https://github.com/astral-sh/uv) which makes running simple python scripts like this a breeze.

### Making the cards

```bash
uv run main.py write "album:a7eaa2055a9aed8141e22377d467cb1e"
```
The format is `<type>:<id>` where type can be one of:
1. album
2. artist
3. song

The id for each can be found in Gelly using the "copy id" function of the dropdown for the item in question. These are just the IDS from the backend. If you use Jellyfin or Subsonic, you should be able to find these IDs fairly easily even without Gelly.

Additionally, it's possible to encode cards with playback controls:
* `stop`
* `next`
* `prev`
* `play-pause`
* 
Are all valid cards as well, and should do the correct thing.

### Listening for card taps

Just run main.py:

```bash
$ uv run main.py
Watching for NFC tags... (Ctrl-C to stop)
Running: ['flatpak', 'run', 'io.m51.Gelly', '--big-player', '--play-album', 'a7eaa2055a9aed8141e22377d467cb1e']
```
That should be all you need. The script will wait for taps and run the appropriate commands.

## Customizing
If you don't use gelly, it should be pretty easy to edit this script to run other commands. See the `find_gelly_bin` function which returns the command
line sequence that will be executed when a card is tapped.

## Likely required system packages

Arch:   ccid acsccid pcsclite pcsc-tools

Debian: libccid libacsccid1 pcscd pcsc-tools

## Other stuff

[pcsc_ndef.py](pcsc_ndef.py) taken from [github.com/Giraut/pcsc-ndef](https://github.com/Giraut/pcsc-ndef)
