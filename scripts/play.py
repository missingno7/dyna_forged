#!/usr/bin/env python3
"""Play the original Dyna Blaster interactively in the PortForge oracle.

Boots straight from the original executable (assets/DYNA.EXE) — the game
needs no boot image and no command tail: its unpack stub runs in 574k
instructions and everything it is configured with (key bindings) it reads
from assets/DYNA.CFG itself. It then runs in pf_view with the game's own
INT 1Ch tick pacing, keyboard input and PC-speaker audio.

The screen is a tweaked VGA mode with no BIOS number: 256x232 unchained
256-colour pixels on a 512x464 raster, double-buffered through the CRTC
start address (see game.json "presentation").

Keys inside the window:
  F9   dump evidence to console
  F10  save screenshot (pf_view_screen.ppm)
  F11  start/stop recording a replay (artifacts/replays/rec_<stamp>...)
  F12  save a full snapshot (artifacts/snapshots/snap_<stamp>.pfsnapshot)

In the game: arrows move, SPACE drops a bomb, LEFT CTRL detonates.

Usage: python scripts/play.py [options]
  --record-replay NAME   record from launch into artifacts/replays/NAME...
  --play-replay NAME     play a recorded replay back in the viewer
  --fast                 with --play-replay: unthrottled playback
  --replay-continue      after playback ends, continue with live input
  --snapshot NAME|PATH   resume from a snapshot instead of a cold boot
  --live-atlas           open the Live Execution Atlas in a second window
  --atlas-interval N     publish an atlas update every N frames (default 1)

Anything else is passed through to pf_view untouched.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORT_FORGE = ROOT / "port_forge"

_pu = importlib.util.spec_from_file_location(
    "player_util", PORT_FORGE / "scripts" / "player_util.py")
player_util = importlib.util.module_from_spec(_pu)
_pu.loader.exec_module(player_util)


def main() -> int:
    if {"-h", "--help"} & set(sys.argv[1:]):
        print(__doc__)
        return 0
    program = ROOT / "assets" / "DYNA.EXE"
    if not program.is_file():
        print(f"missing {program} — see assets/README.md")
        return 1
    subprocess.run([sys.executable, "build.py", "--no-tests", "--targets", "pf_view"],
                   check=True, cwd=PORT_FORGE)
    args = player_util.resolve_artifacts(ROOT, sys.argv[1:])
    # --live-atlas takes the atlas directory; supply this repo's by default so
    # the flag needs no path (port_forge docs/20).
    if "--live-atlas" in args:
        at = args.index("--live-atlas")
        if at + 1 >= len(args) or args[at + 1].startswith("--"):
            atlas = ROOT / "artifacts" / "atlas.pfatlas"
            if not atlas.is_dir():
                print(f"no atlas at {atlas} — build one first:\n"
                      f"  python scripts/atlas.py build")
                return 1
            args.insert(at + 1, str(atlas))
    return subprocess.run(
        [str(PORT_FORGE / "build" / "pf_view.exe"), str(program),
         str(ROOT / "assets"), str(ROOT / "game.json"), *args],
        cwd=ROOT).returncode


if __name__ == "__main__":
    sys.exit(main())
