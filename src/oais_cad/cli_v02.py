"""Run with python -m oais_cad.cli_v02 examples/v02_walls.json build/v02."""
import json
import sys
from pathlib import Path
from .export_v02 import export_plan
from .v02 import IntentError

def main():
    if len(sys.argv)!=3:
        print("Usage: python -m oais_cad.cli_v02 INPUT.json OUTPUT_DIR",file=sys.stderr)
        return 2
    try:
        spec=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        print(json.dumps(export_plan(spec,sys.argv[2]),indent=2))
        return 0
    except (ValueError,OSError,IntentError) as exc:
        print(f"FAILED CLOSED: {exc}",file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
