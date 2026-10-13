"""Export a review-only SVG from validated 2D CAD strips."""
import json
import sys
from pathlib import Path
from .visual_review_v02 import export

def main():
    if len(sys.argv) != 3:
        print("usage: python -m oais_cad.preview_cli_v02 INPUT.json OUTPUT.svg", file=sys.stderr)
        return 2
    try:
        source = Path(sys.argv[1])
        target = Path(sys.argv[2])
        spec = json.loads(source.read_text(encoding="utf-8"))
        export(spec, target)
        print(str(target))
        return 0
    except (OSError, ValueError) as exc:
        print("FAILED CLOSED: " + str(exc), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
