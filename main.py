#!/usr/bin/env python3
import subprocess
import sys
import time
from pathlib import Path

import ndef
from smartcard.CardMonitoring import CardMonitor, CardObserver

PCSC_NDEF = Path(__file__).parent / "pcsc_ndef.py"


def find_gelly_bin() -> list[str]:
    result = subprocess.run(
        ["flatpak", "info", "io.m51.Gelly"],
        capture_output=True,
    )
    if result.returncode == 0:
        return ["flatpak", "run", "io.m51.Gelly"]

    result = subprocess.run(
        ["which", "gelly"],
        capture_output=True,
    )
    if result.returncode == 0:
        return ["gelly"]

    return []


def build_command(card_text: str) -> list[str]:
    base_cmd = find_gelly_bin()
    if not base_cmd:
        print(
            "Gelly not found, do you have it installed?",
            file=sys.stderr,
            flush=True,
        )
        return []
    parts = card_text.split(":", 1)
    if len(parts) == 2:
        scheme, id = parts
    elif len(parts) == 1:
        scheme, id = parts[0], ""
    else:
        print("Invalid card text:", card_text, file=sys.stderr, flush=True)
        return []
    match scheme:
        case "album":
            return [*base_cmd, "--big-player", "--play-album", id]
        case "artist":
            return [*base_cmd, "--big-player", "--play-artist", id]
        case "song":
            return [*base_cmd, "--big-player", "--play-song", id]
        case "next":
            return [*base_cmd, "--next"]
        case "prev":
            return [*base_cmd, "--prev"]
        case "play-pause":
            return [*base_cmd, "--play-pause"]
        case "stop":
            return [*base_cmd, "--stop"]
        case _:
            print("Unknown scheme:", scheme, file=sys.stderr, flush=True)
            return []


def read_tag_text() -> str | None:
    result = subprocess.run(
        [sys.executable, PCSC_NDEF, "-t2", "read"],
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    try:
        for record in ndef.message_decoder(result.stdout):
            if isinstance(record, ndef.TextRecord):
                return record.text
    except Exception:
        return None
    return None


def write_tag_text(text) -> bool:
    ndef_data = b"".join(ndef.message_encoder([ndef.TextRecord(text)]))
    result = subprocess.run(
        [sys.executable, PCSC_NDEF, "-t2", "write"],
        input=ndef_data,
        capture_output=True,
    )
    return result.returncode == 0


class ReadObserver(CardObserver):
    def update(self, observable, handlers):
        _ = observable
        added, _ = handlers
        if not added:
            return
        time.sleep(0.2)
        text = read_tag_text()
        if text is None:
            return
        cmd = build_command(text)
        if cmd:
            print(f"Running: {cmd}", file=sys.stderr, flush=True)
            subprocess.run(cmd)
        else:
            print(text, flush=True)


class WriteObserver(CardObserver):
    def __init__(self, text):
        self.text = text
        self.done = False

    def update(self, observable, handlers):
        _ = observable
        added, _ = handlers
        if not added or self.done:
            return
        time.sleep(0.2)
        if write_tag_text(self.text):
            print(f"Written: {self.text}", flush=True)
            self.done = True
        else:
            print("Write failed", file=sys.stderr, flush=True)


def watch_mode():
    observer = ReadObserver()
    monitor = CardMonitor()
    monitor.addObserver(observer)
    print("Watching for NFC tags... (Ctrl-C to stop)", file=sys.stderr)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.deleteObserver(observer)


def write_mode(text):
    observer = WriteObserver(text)
    monitor = CardMonitor()
    monitor.addObserver(observer)
    print("Tap a tag to write... (Ctrl-C to cancel)", file=sys.stderr)
    try:
        while not observer.done:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        monitor.deleteObserver(observer)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "write":
        if len(sys.argv) < 3:
            print("Usage: main.py write <text>", file=sys.stderr)
            sys.exit(1)
        write_mode(sys.argv[2])
    else:
        watch_mode()
