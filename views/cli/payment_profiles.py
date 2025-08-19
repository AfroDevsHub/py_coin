from models.user.accounts import Account
from typing import cast
from inquirer import Text, prompt, List

from lib.utils.constants.responses import ServiceStatus
from lib.utils.constants.users import CardType
from services.user import UserService

def display_add_payment_profile(account: Account) -> None:
    card_types = [
        List(
            "card_type",
            "Select Card Type",
            choices=[card_type.name for card_type in CardType],
        )
    ]
    card_type = cast(dict[str, str], prompt(card_types))

    pin_text = [Text("pin", "Enter PIN")]
    pin = cast(dict[str, str], prompt(pin_text))
    response = UserService().create_payment_profile(
        account.id,
        getattr(CardType, card_type["card_type"]),
        pin["pin"],
    )
    print(f"Response: {response.message} | Status: {response.status}")
    if response.status != ServiceStatus.SUCCESS:
        print("[❌] Failed to create payment profile.")
    else:
        print("[✅] Payment profile created successfully.")