"""Generate evidence-only report. Example: python scripts/pdf_evidence_report.py plan.pdf build/pdf"""
import argparse
from oais_cad.pdf_report import make_pdf_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("--tokens", nargs="*", default=[])
    args = parser.parse_args()
    report = make_pdf_report(args.source, args.output, args.tokens)
    print(f"Evidence report: {len(report['pages'])} page(s); decision={report['decision']}")


if __name__ == "__main__":
    main()
