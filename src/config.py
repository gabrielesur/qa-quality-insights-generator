"""Configuration helpers for QA Quality Insights Generator."""
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    jira_base_url: str | None
    jira_user: str | None
    jira_api_token: str | None
    default_project: str | None


def load_config() -> Config:
    return Config(
        jira_base_url=os.getenv("JIRA_BASE_URL"),
        jira_user=os.getenv("JIRA_USER"),
        jira_api_token=os.getenv("JIRA_API_TOKEN"),
        default_project=os.getenv("DEFAULT_PROJECT"),
    )
