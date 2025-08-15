"""Responses: Contains Constants, Enumerations and Other Static data."""

from enum import Enum


class ServiceStatus(Enum):
    """Enumeration of Service Statuses."""

    SUCCESS = "Success"
    ERROR = "Error"
    WARNING = "Warning"
    INFO = "Info"
