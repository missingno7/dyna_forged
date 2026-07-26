#!/usr/bin/env python3
"""Play Dyna Blaster through the project-declared PortForge runtime.

Plain invocation selects the manifest default (currently ``oracle``).

Target runner options:
  --record-replay NAME   record into artifacts/replays/
  --play-replay NAME     play a recorded replay
  --fast                 run replay playback unthrottled
  --replay-continue      continue with live input after playback
  --snapshot NAME|PATH   resume from a snapshot
  --live-atlas           attach the project's Live Execution Atlas
  --atlas-interval N     publish an Atlas update every N frames

Anything after ``--`` is forwarded verbatim to the selected runner.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORT_FORGE = ROOT / "port_forge"
sys.path.insert(0, str(PORT_FORGE / "scripts"))
import player_runtime  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    source = list(sys.argv[1:] if argv is None else argv)
    if player_runtime.help_requested(source):
        print(player_runtime.render_help(__doc__))
        return 0

    selection = player_runtime.select_runtime(ROOT, source)
    program = ROOT / "assets" / "DYNA.EXE"
    runner = PORT_FORGE / "build" / "pf_view.exe"
    if not selection.dry_run:
        player_runtime.require_artifact(program, selection)
        if selection.no_build:
            player_runtime.require_artifact(runner, selection)
        else:
            subprocess.run(
                [
                    sys.executable,
                    "build.py",
                    "--no-tests",
                    "--targets",
                    "pf_view",
                ],
                check=True,
                cwd=PORT_FORGE,
            )

    args = player_runtime.prepare_runner_args(ROOT, selection)
    game = json.loads((ROOT / "game.json").read_text(encoding="utf-8"))
    return player_runtime.run_selected(
        selection,
        [
            str(runner),
            str(program),
            str(ROOT / "assets"),
            str(ROOT / "game.json"),
            *args,
        ],
        cwd=ROOT,
        identity=[
            f"program identity: sha256:{game['program']['sha256']}",
            "PortForge runtime: included",
        ],
    )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (
        OSError,
        player_runtime.PlayerConfigError,
        subprocess.CalledProcessError,
    ) as error:
        print(f"play.py: {error}", file=sys.stderr)
        sys.exit(1)
