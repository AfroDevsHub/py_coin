"""CLI: Command Line Types, Data-Classes and Typed Dicts."""

# from argparse import Namespace
from pydantic import BaseModel


class DataArgs(BaseModel):
    """Type Check for CLI Arguments."""

    uuid: str | None
    sender: str | None
    receiver: str | None
    sender_signiture: str | None
    receiver_signiture: str | None
    data: bool | None


class TypeArgs(BaseModel):
    """Type Check for CLI Arguments."""

    transaction: bool
    contract: bool
    block: bool
    user: bool


class Args(BaseModel):
    """Type Check for CLI Arguments."""

    command: str
