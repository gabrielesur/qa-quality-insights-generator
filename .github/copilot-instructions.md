# Copilot / AI Agent Instructions

Purpose: Give AI coding agents the minimal, actionable context needed to contribute quickly to this repository.

Big picture
- **Goal:** Generate monthly QA quality-insights reports by aggregating data (initially Jira) and applying simple, rule-based logic to surface trends and risks. See [README.md](README.md).
- **Runtime & entrypoint:** CI runs `python src/main.py` on a schedule — treat `src/main.py` as the canonical entrypoint for the monthly report. See [.github/workflows/rspec.yml](.github/workflows/rspec.yml).

What to expect in the codebase
- The repo is currently documentation- and planning-first (early/experimental). Expect the implementation to live under `src/` and dependencies in `requirements.txt` if present.
- Data sources: Jira is the first target. Integrations (eazyBI, metrics tools) are planned but not implemented.
- Output format: human-readable Quality Insights (Markdown or similar) generated monthly.

Key files to review before editing
- [README.md](README.md) — project goals, MVP, scope and status.
- [.github/workflows/rspec.yml](.github/workflows/rspec.yml) — shows scheduled CI job that runs `python src/main.py` and installs `requirements.txt` when present.
- `requirements.txt` — optional; CI installs it if present. Add dependencies here when adding new Python packages.
- `src/main.py` — expected script entrypoint (create if missing).

Local developer workflow (what CI does; reproduce locally)
1. Ensure Python 3.x is used (CI sets `python-version: '3.x'`).
2. Install deps and run the script:

```bash
python -m pip install --upgrade pip
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
python src/main.py
```

Project-specific conventions and patterns
- Keep the implementation lightweight and rule-based for the MVP (simple aggregations, counts, month-over-month diffs). Prefer clear, inspectable logic over heavy ML or opaque heuristics.
- Prefer generating Markdown reports so they can be easily reviewed in PRs or published to Confluence/Slack in the future.
- If adding new integrations, make them opt-in via configuration (do not hard-code credentials or endpoints). Document required environment variables or secrets in the top-level README.

Integration notes
- CI schedule: the workflow is scheduled to run monthly (6:00 UTC on the 1st). Changes to the report generation may need a way to run for arbitrary months locally — add CLI flags like `--month YYYY-MM` to `src/main.py`.
- Secrets & credentials: the repo currently has no secret management patterns defined. Use GitHub Actions secrets for credentials when adding real integrations; document any required secrets in README.

When editing or extending this repo
- Add or update `requirements.txt` when introducing new packages.
- Add tests under a `tests/` directory and a GitHub Actions job when tests exist.
- Keep changes small and reviewable; provide a sample output Markdown with PRs so reviewers can validate the insights.

If anything is missing from these notes, tell me which files or workflows you expect and I will expand the instructions.
