from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class APIHealthReponse(BaseModel):
    api: str
    status: str

class DatabaseCheckResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

class HealthCheckResponse(BaseModel):
    database: DatabaseCheckResponse = Field(
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
    api: dict[str, str] = Field(
        examples=[
            {"status": "ACTIVE", "api": "Auth Service"},
            {"status": "INACTIVE", "api": "Payment Service"},
        ],
    )


class VersionCheckResponse(BaseModel):
    version: str = "Unknown Version"
    date: str = datetime.now().strftime("%Y-%m-%d")
    author: str = "Unknown Author"
