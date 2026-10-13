"""CLI for unified evidence-only PDF pipeline."""
import argparse
from oais_cad.pdf_pipeline import run_pdf_pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("--tokens", nargs="*", default=[])
    parser.add_argument("--radius", type=float, default=25)
    parser.add_argument("--max-lines", type=int, default=2000)
    parser.add_argument("--max-pairs", type=int, default=100000)
    args = parser.parse_args()
    report = run_pdf_pipeline(args.source, args.output, tokens=args.tokens, radius=args.radius,
                              max_lines=args.max_lines, max_pairs=args.max_pairs)
    print(f"pages={len(report['pages'])}; decision={report['decision']}; source_sha256={report['source_sha256']}")


if __name__ == "__main__":
    main()
