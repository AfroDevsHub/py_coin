"""Test-Utils: Configure Utils Module."""

from uuid import uuid4
from typing import Any
from sqlalchemy.orm import Session

DATA = {
    "GITHUB": "https://github.com/example_username",
    "FACEBOOK": "https://www.facebook.com/example.username",
    "TWITTER": "https://twitter.com/example_username",
    "INSTAGRAM": "https://www.instagram.com/example_username",
    "LINKEDIN": "https://www.linkedin.com/in/example-username",
    "PINTEREST": "https://www.pinterest.com/example_username",
    "TIKTOK": "https://www.tiktok.com/@example_username",
    "REDDIT": "https://www.reddit.com/user/example_username",
    "DISCORD": "https://www.discord.com/users/123456789",
    "TELEGRAM": "https://t.me/example_username",
    "YOUTUBE": "https://www.youtube.com/user/example-username",
    "SLACK": "https://example-team.slack.com/",
    "TWITCH": "https://www.twitch.tv/example_username",
    "SPOTIFY": "https://open.spotify.com/user/example_user_id",
    "SOUNDCLOUD": "https://soundcloud.com/example_username",
}


def generate_socials(key: str | None = None) -> str | dict[str, str]:
    """Returns Test Social Media Link."""

    if not key:
        return DATA
    return DATA[key]


def setup_test_commit(models: list[Any], session: Session):
    """Abstraction of the persistence functionality."""

    session.add_all(models)
    session.commit()


def run_test_teardown(models: list[Any], session: Session):
    """Abstraction of the Clearing of the Test Database."""

    for model in models:
        session.delete(model)
    session.commit()


def check_invalid_ids() -> list[Any]:
    """Returns a list of invalid ID to Test."""

    return [uuid4(), "Invalid ID String.", 1, None]
