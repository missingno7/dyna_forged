# dyna_forged

**Dyna Blaster** (Hudson Soft, published by Ubi Soft, 1991-1992) as a
PortForge target game. This repository owns everything game-specific; the
[port_forge](port_forge/) submodule owns everything general — anything
reusable graduates into PortForge itself rather than living here.

## Run it

```bash
python scripts/play.py
```

That cold-loads the original executable in the PortForge oracle and opens
the game in a window. No boot image, no import step, no command tail: the
unpack stub runs in 574k instructions and everything the game is configured
with (its key bindings) it reads from `assets/DYNA.CFG` itself.

Arrows move, SPACE drops a bomb, LEFT CTRL detonates. Inside the window F10
saves a screenshot, F11 records a replay and F12 saves a snapshot.

Headless, for growing the services layer against real evidence:

```bash
python scripts/run_game.py 200
```

## The screen is a mode the BIOS has no number for

Dyna Blaster sets BIOS mode 12h (640x480x16 planar) and then takes the
hardware apart: it rewrites the CRTC and turns on the attribute controller's
8-bit-colour bit, which makes the four planes hold **one byte per pixel**
indexing the DAC directly, with the 16 attribute palette registers out of the
path entirely. That is the unchained 256-colour "Mode X" family.

The raster it programs is **512x464** — 64 character clocks of 8 dots, 464
active scan lines. The picture inside it is **256x232**, because a
256-colour pixel costs two dot clocks and Maximum Scan Line 1 spends two scan
lines per row. Pixels come out square (256:232 = 1.103, and the 512 dots of
a 25.175 MHz clock over 464 of 524 lines works out to the same 1.103 of a 4:3
screen). The playfield is 15x11 tiles of 16x16 pixels, which checks.

The buffer is double-buffered by CRTC start address at a 64-byte-per-plane
stride, flipped between 2540h and 9F40h once per tick.

PortForge could not present any of this when this repository started; the
support was added there, not here (`dos_rm: 256-colour unchained VGA`).

## Pacing: 18.2 Hz, on the BIOS tick

The game never programs PIT channel 0, so it runs on the BIOS 18.2065 Hz
tick — and it hooks **INT 1Ch**, the BIOS user tick hook, not INT 08h. Its
ISR at `1010:1355` sets the frame flag `[1975:204F]` as its first act and
counts 18 ticks to a second (`cmp word [204C],12h`) to drive the level
clock in the HUD. One pass of the flag gate at `1010:1643` is therefore one
displayed frame, at one timer IRQ each. All of that is recorded in
[game.json](game.json).

## Layout

```text
dyna_forged/
├── port_forge/       # PortForge framework (git submodule)
├── assets/           # original game data (not committed — see assets/README.md)
├── game.json         # program fingerprint, frame model, presentation facts
├── scripts/          # game workflows built on PortForge tools
└── artifacts/        # generated snapshots/replays/evidence (not committed)
```
