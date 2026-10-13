"""Command-line entry point: python -m oais_cad.cli specification.json output/"""
import json
import sys
from pathlib import Path
from .engine import ValidationError, generate

def main():
    if len(sys.argv) != 3:
        print("Usage: python -m oais_cad.cli SPEC.json OUTPUT_DIR",file=sys.stderr)
        return 2
    try:
        spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        print(json.dumps(generate(spec,sys.argv[2]),indent=2))
        return 0
    except (ValueError, OSError, ValidationError) as error:
        print(f"FAILED CLOSED: {error}",file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
