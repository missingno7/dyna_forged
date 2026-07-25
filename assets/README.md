# assets/

Original Dyna Blaster game data. Not committed — the files are the
copyrighted 1991-1992 Hudson Soft / Ubi Soft release; this repository holds
only the port. Fingerprints are pinned in [../game.json](../game.json).

| file | role |
|---|---|
| `DYNA.EXE` | the game. A 42096-byte self-extracting MZ image (32-byte header, zero relocations, entry `0991:000E`) whose stub hands control to the game proper at `1010:0000`. This is what PortForge boots. |
| `INTRO.EXE` | the separate intro sequence. Not on the play path. |
| `DYNA.CFG` | 28 bytes of key bindings, read once at startup and rewritten only by the game's own SETUP screen. |
| `GFX/NN.IMG` | the graphics: IFF ILBM, 320x200, 8 bitplanes (256 colours), ByteRun1 compressed, 5:6 pixel aspect — the Amiga heritage showing. The game scans the loaded file for its `BODY` chunk and unpacks from there. |
| `DYNA.COD` | the plain-text level password table (`LEVEL 1.1  MBHLJQHY` …). |
| `DEMO.DAT` | the attract-mode demo script. |
| `DIGI.DAT` | digitized sound samples (Sound Blaster). |
| `MUSIC`, `MUSIC.DAT` | music data. |
| `PAL` | a text-format palette dump. |
| `PIC` | 64000 bytes = one 320x200 mode-13h screen, used by `INTRO.EXE`. |

The game opens its data with DOS paths in lower case and with backslashes
(`gfx\19.img`), so the directory layout matters: `GFX/` must sit beside
`DYNA.EXE`.
