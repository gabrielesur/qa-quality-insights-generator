"""Entrypoint for generating monthly QA quality insights.

Usage (local):

    python src/main.py --month 2026-01

Available options: `--month YYYY-MM` and `--dry-run` (print to stdout).
"""
from __future__ import annotations
import argparse
from pathlib import Path
from src.config import load_config
from src.jira_client import JiraClient
from src.report_generator import ReportGenerator


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate monthly QA quality insights")
    p.add_argument("--month", required=True, help="Target month in YYYY-MM format")
    p.add_argument("--project", required=False, help="Jira project key (overrides DEFAULT_PROJECT)")
    p.add_argument("--dry-run", action="store_true", help="Do not write files; print report to stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    cfg = load_config()

    client = JiraClient(cfg.jira_base_url, cfg.jira_user, cfg.jira_api_token)
    project = args.project or cfg.default_project

    issues = client.fetch_issues(args.month, project=project)

    rg = ReportGenerator()
    report = rg.generate(issues, args.month)

    if args.dry_run:
        print(report)
    else:
        out_dir = Path("samples")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"report_{args.month}.md"
        out_file.write_text(report, encoding="utf8")
        print(f"Wrote report to {out_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
