"""Report generation helpers to produce Markdown quality insights.

This module provides a compact, rule-based generator used by the MVP. Keep
rules simple and inspectable so reviewers can reason about the signals being
reported.
"""
from typing import Iterable, Optional
from collections import Counter


class ReportGenerator:
    def generate(self, issues: Iterable[dict], month: str, previous_issues: Optional[Iterable[dict]] = None) -> str:
        """Generate a Markdown report for `month`.

        Optional `previous_issues` can be provided to produce a simple
        month-over-month comparison.
        """
        issues = list(issues)
        total = len(issues)

        # Severity distribution
        severity_counts: dict[str, int] = {}
        for it in issues:
            p = it.get("priority") or "Unknown"
            severity_counts[p] = severity_counts.get(p, 0) + 1

        # Recurring issues by exact summary match (simple heuristic)
        summary_counts = Counter((it.get("summary") or "").strip().lower() for it in issues)
        recurring = [(s, c) for s, c in summary_counts.items() if s and c > 1]

        lines = []
        lines.append(f"# QA Quality Insights — {month}")
        lines.append("")
        lines.append(f"**Total issues found:** {total}")
        lines.append("")

        lines.append("**Severity distribution:**")
        lines.append("")
        for sev, cnt in sorted(severity_counts.items(), key=lambda x: -x[1]):
            lines.append(f"- **{sev}:** {cnt}")

        # Month-over-month comparison (very small, rule-based)
        if previous_issues is not None:
            prev_total = len(list(previous_issues))
            delta = total - prev_total
            pct = None
            if prev_total > 0:
                pct = (delta / prev_total) * 100

            lines.append("")
            lines.append("**Month-over-month:**")
            if pct is None:
                lines.append(f"- Current: {total}, Previous: {prev_total} (no percent change)")
            else:
                sign = "+" if delta >= 0 else ""
                lines.append(f"- Current: {total}, Previous: {prev_total} ({sign}{delta} / {sign}{pct:.0f}% change)")

            # Simple risk signal: sizable increase
            if pct is not None and pct >= 20:
                lines.append("")
                lines.append(
                    "> **Risk:** Issues increased significantly month-over-month — consider prioritizing investigation."
                )

        # Recurring issues
        if recurring:
            lines.append("")
            lines.append("**Recurring issues detected:**")
            lines.append("")
            for s, c in sorted(recurring, key=lambda x: -x[1])[:5]:
                lines.append(f"- {c} occurrences — {s}")

        # Example items
        if total > 0:
            lines.append("")
            lines.append("**Example issues:**")
            lines.append("")
            for it in issues[:5]:
                lines.append(f"- {it.get('key')} — {it.get('summary')}")

        return "\n".join(lines)
