"""App: Ingress Point."""

from enum import Enum
from typing import cast
from inquirer import prompt, List
from pydantic import BaseModel

from lib.interfaces.responses import ServiceResponse
from lib.interfaces.user.accounts import UpdateAccountData
from lib.interfaces.user.payments import UpdatePaymentProfileData
from lib.interfaces.user.users import UpdateUserData
from lib.utils.constants.responses import ServiceStatus
from services.user import UserService
from views.cli.manage_account import display_manage_account_sections
from views.cli.payment_profiles import display_add_payment_profile
from views.cli.user_account import display_account_sections
from views.cli.authentication import handle_intro


def handle_user_services_input(answer: dict[str, str], user_id: str) -> ServiceResponse:
    match answer["user_services"]:
        case "Create Account":
            print(f"[{user_id} 🔐] Create Account Service Selected.")
            response = UserService().create_user_account(user_id)
            print(f"Response: {response.message} | Status: {response.status}")
            return response

        case "View Account" | "Add Payment Profile" | "Manage Account":
            print(f"[{user_id} 🔐] View Account Service Selected.")
            response = UserService().get_user_accounts(user_id)
            print(f"Response: {response.message} | Status: {response.status}")
            return response
        case _:
            return ServiceResponse(
                message="Invalid user service selected.", status=ServiceStatus.ERROR
            )


def handle_auth_input(answer: dict[str, str]) -> ServiceResponse:
    match answer["auth"]:
        case "Login":
            print("[🔐] Login Service Selected.")
            response = UserService().login_user(answer["username"], answer["password"])
            print(f"Response: {response.message} | Status: {response.status}")
            return response

        case "Logout":
            print("[🔐] Logout Service Selected.")
            response = UserService().logout_user()
            print(f"Response: {response.message} | Status: {response.status}")
            return response

        case _:
            return ServiceResponse(
                message="Invalid auth action selected.", status=ServiceStatus.ERROR
            )


def main() -> bool:
    """CLI Interface."""

    token: str | None = None
    user_id: str | None = None
    while True:
        intro = [
            List(
                "intro",
                "Welcome to PY Coin",
                choices=["Register User", "Login User", "Exit"],
            )
        ]

        if not token or not user_id:
            answers = cast(dict[str, str], prompt(intro))
            response = handle_intro(answers)
            print(f"Response: {response.message} | Status: {response.status}")

            if (
                response.status == ServiceStatus.INFO
                and response.data
                and response.data.get("exit")
            ):
                print("[✅] Thank you for using PY Coin. Goodbye!")
                return False

            if response.status == ServiceStatus.ERROR:
                print("[❌] An error occurred. Please try again.")
                continue

            if answers["intro"] == "Register User":
                print("[🔐] User registered successfully.")
                continue

            if (
                not response.data
                or "user" not in response.data
                or "login" not in response.data
            ):
                print("[❌] User ID/Token not found.")
                continue

            print(f"[🔐] User ID: {response.data['user'].id}")
            user_id = response.data["user"].id
            token = response.data["login"].authentication_token
            continue

        services = [
            List(
                "services",
                "Select a service",
                choices=["User", "Block Chain", "Exit"],
            )
        ]

        answer = cast(dict[str, str], prompt(services))
        if answer["services"] == "User":
            print("[🔐] User Service Selected.")
            user_services = [
                List(
                    "user_services",
                    f"[{user_id}] Select a Service",
                    choices=[
                        "Create Account",
                        "Manage Account",
                        "View Account",
                        "Add Payment Profile",
                    ],
                )
            ]
            answer = cast(dict[str, str], prompt(user_services))
            response = handle_user_services_input(answer, user_id)
            if response.status != ServiceStatus.SUCCESS:
                print("[❌] Failed to create user account.")
                continue

            if (
                not response.data
                or "account" not in response.data
                or not response.data["account"]
            ) and answer["user_services"] == "Create Account":
                print("[❌] No account found for this user.")
                continue

            if answer["user_services"] == "Create Account":
                print("[🔐] User account created successfully.")
                continue

            if (
                not response.data
                or "accounts" not in response.data
                or not response.data["accounts"]
            ):
                print("[❌] No account(s) found for this user.")
                continue

            accounts = [
                List(
                    "accounts",
                    f"[{user_id}] Select an Account",
                    choices=[
                        f"Account ID: {account.id} | Created: {account.created_date}"
                        for account in response.data["accounts"]
                    ],
                )
            ]

            account_answer = cast(dict[str, str], prompt(accounts))
            print(f"Selected Account: {account_answer['accounts']}")

            account_id = account_answer["accounts"].split(": ")[1].split(" | ")[0]
            print(f"Account ID: {account_id}")
            account = UserService().get_user_account(account_id)

            if (
                account.status != ServiceStatus.SUCCESS
                or not account.data
                or "account" not in account.data
            ):
                print("[❌] Failed to retrieve account.")
                continue

            if answer["user_services"] == "View Account":
                display_account_sections(account.data["account"])

            if answer["user_services"] == "Add Payment Profile":
                display_add_payment_profile(account.data["account"])

            if answer["user_services"] == "Manage Account":
                display_manage_account_sections(account.data["account"])


            continue
        elif answer["services"] == "Block Chain":
            print(f"[{user_id} 🔗] Block Chain Service Selected.")
            block_chain_services = [
                List(
                    "block_chain_services",
                    "Select a Service",
                    choices=["Contract Services", "Transaction Services"],
                )
            ]
            answer = cast(dict[str, str], prompt(block_chain_services))

        elif answer["services"] == "Exit":
            print("[✅] Thank you for using PY Coin. Goodbye!")
            return False

if __name__ == "__main__":
    main()
