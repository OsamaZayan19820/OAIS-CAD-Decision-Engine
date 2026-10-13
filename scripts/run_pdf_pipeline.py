"""CLI for unified evidence-only PDF pipeline."""
import argparse
from oais_cad.pdf_pipeline import run_pdf_pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("--tokens", nargs="*", default=[])
    parser.add_argument("--radius", type=float, default=25)
    args = parser.parse_args()
    report = run_pdf_pipeline(args.source, args.output, tokens=args.tokens, radius=args.radius)
    print(f"pages={len(report['pages'])}; decision={report['decision']}; source_sha256={report['source_sha256']}")


if __name__ == "__main__":
    main()
