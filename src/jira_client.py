"""Simple Jira client wrapper used by the MVP.

This module intentionally keeps behavior small and inspectable: it provides a
single `JiraClient` class with a `fetch_issues(month, project)` method that
returns a list of issue dicts. Real network calls are implemented with
`requests` but callers should be prepared for empty results when credentials
are not provided (useful for local dry-runs).
"""
from __future__ import annotations
import os
from typing import List
import requests


class JiraClient:
    def __init__(self, base_url: str | None, user: str | None, api_token: str | None):
        self.base_url = base_url
        self.user = user
        self.api_token = api_token

    def authenticated(self) -> bool:
        return bool(self.base_url and self.user and self.api_token)

    def fetch_issues(self, month: str, project: str | None = None) -> List[dict]:
        """Fetch issues for the given month (format: YYYY-MM).

        Returns a list of simplified issue dicts. If authentication is missing
        this returns an empty list so the rest of the pipeline can run in
        dry-run mode.
        """
        if not self.authenticated():
            return []

        # Minimal example using Jira Cloud API search endpoint.
        jql_parts = [f"created >= {month}-01", f"created < {month}-32"]
        if project:
            jql_parts.insert(0, f"project = {project}")
        jql = " AND ".join(jql_parts)

        url = f"{self.base_url.rstrip('/')}/rest/api/2/search"
        params = {"jql": jql, "maxResults": 100}
        auth = (self.user, self.api_token)

        resp = requests.get(url, params=params, auth=auth, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        issues = []
        for it in data.get("issues", []):
            fields = it.get("fields", {})
            issues.append(
                {
                    "key": it.get("key"),
                    "summary": fields.get("summary"),
                    "created": fields.get("created"),
                    "priority": (fields.get("priority") or {}).get("name"),
                    "issuetype": (fields.get("issuetype") or {}).get("name"),
                }
            )

        return issues
