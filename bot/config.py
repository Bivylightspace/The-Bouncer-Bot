from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent


class Settings:
    """Class to hold application's config values."""
    APP_NAME: str = config("APP_NAME", default="The Bouncer Bot")
    APP_VERSION: str = config("APP_VERSION", default="0.1.0")
    APP_DESCRIPTION: str = config(
        "APP_DESCRIPTION", default="Remove/Add users from channels")

    SLACK_BOT_TOKEN = config("SLACK_BOT_TOKEN", "")
    SLACK_SIGNING_SECRET = config("SLACK_SIGNING_SECRET", "")

    TRENCHES = config("TRENCHES", "trenches")


settings = Settings()
