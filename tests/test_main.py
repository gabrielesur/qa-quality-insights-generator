from src.report_generator import ReportGenerator


def test_report_generator_simple():
    issues = [
        {"key": "TST-1", "summary": "First", "priority": "High"},
        {"key": "TST-2", "summary": "Second", "priority": "Low"},
    ]
    rg = ReportGenerator()
    out = rg.generate(issues, "2026-01")
    assert "Total issues found" in out
    assert "High" in out


def test_report_generator_month_over_month_and_recurring():
    prev = [
        {"key": "TST-0", "summary": "Flaky endpoint fails", "priority": "Medium"},
    ]

    issues = [
        {"key": "TST-1", "summary": "Flaky endpoint fails", "priority": "High"},
        {"key": "TST-2", "summary": "Flaky endpoint fails", "priority": "High"},
        {"key": "TST-3", "summary": "Other bug", "priority": "Low"},
    ]

    rg = ReportGenerator()
    out = rg.generate(issues, "2026-01", previous_issues=prev)

    # month-over-month block present and shows an increase
    assert "Month-over-month" in out
    assert "increased" in out or "change" in out

    # recurring issue detected ("flaky endpoint fails" appears multiple times)
    assert "recurring" in out.lower() or "occurrences" in out
