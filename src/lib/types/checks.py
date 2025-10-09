from datetime import datetime
from pydantic import BaseModel, Field

class CheckResponse(BaseModel):
    timestamp: str = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

class HealthCheckResponse(CheckResponse):
    database: dict[str, str] = Field(
        examples=[
            {
                "LoginHistory": "ACTIVE",
                "Card": "ACTIVE",
                "User": "ACTIVE",
                "PaymentProfile": "ACTIVE",
                "SettingsProfile": "ACTIVE",
                "UserProfile": "ACTIVE",
                "Account": "ACTIVE",
                "Block": "ACTIVE",
                "Contract": "ACTIVE",
                "Transaction": "ACTIVE",
            }
        ]
    )


class VersionCheckResponse(CheckResponse):
    version: str
    date: str
    author: str
