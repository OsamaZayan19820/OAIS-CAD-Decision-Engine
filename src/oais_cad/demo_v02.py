"""Reproducible, unapproved 2D CAD demonstration."""
import argparse
import json
from pathlib import Path
from .publish_solids_v02 import publish_solid_plan
from .verify_release_v02 import verify_release

SAMPLE={
    "units":"mm",
    "walls":[{"id":"W1","start":[0,0],"end":[5000,0],"thickness":200}],
    "openings":[{"id":"D1","wall_id":"W1","type":"door","offset":1000,"width":900}],
}

def main(argv=None):
    parser=argparse.ArgumentParser(description="Generate and verify a V0.2 2D wall DXF demo")
    parser.add_argument("--out",default="build/oais_demo_v02")
    args=parser.parse_args(argv)
    output=Path(args.out)
    publish_solid_plan(SAMPLE,output)
    verified=verify_release(output)
    print(json.dumps({"release":str(output),"verification":verified},sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
