#!/usr/bin/env python3
"""Run Dyna Blaster headlessly in the PortForge oracle — the fail-loud loop.

Cold-boots assets/DYNA.EXE, attaches the DOS/BIOS services layer, and runs
until the game blocks on input, exits, hits unimplemented territory
(classified evidence naming the exact call), or reaches the instruction
limit. Whatever graphics mode is current is written out as a screenshot.

Note that this path free-runs the interpreter with IRQ0 paced by the
instruction count, NOT the game's semantic frame loop — it is the discovery
tool. Use scripts/play.py to actually play.

Usage: python scripts/run_game.py [max_minstr] [scancode_hex...]
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORT_FORGE = ROOT / "port_forge"


def main() -> int:
    if {"-h", "--help"} & set(sys.argv[1:]):
        print(__doc__)
        return 0
    program = ROOT / "assets" / "DYNA.EXE"
    if not program.is_file():
        print(f"missing {program} — see assets/README.md")
        return 1
    subprocess.run([sys.executable, "build.py", "--no-tests", "--targets", "pf_run"],
                   check=True, cwd=PORT_FORGE)
    result = subprocess.run(
        [str(PORT_FORGE / "build" / "pf_run.exe"), str(program),
         str(ROOT / "assets"), *sys.argv[1:]], cwd=ROOT)
    ppm = ROOT / "pf_run_screen.ppm"
    if ppm.is_file():
        try:
            from PIL import Image
            png = ppm.with_suffix(".png")
            im = Image.open(ppm)
            im.resize((im.width * 2, im.height * 2), Image.NEAREST).save(png)
            print(f"screenshot: {png}")
        except ImportError:
            print(f"screenshot: {ppm} (install Pillow for .png)")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
