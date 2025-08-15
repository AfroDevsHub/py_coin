"""App: Ingress Point."""

import os
from typing import cast
from inquirer import Text, prompt, List
import requests

from lib.interfaces.responses import ServiceResponse
from lib.utils.constants.responses import ServiceStatus
from lib.utils.constants.users import Country, LoginMethod
from services.authentication import AuthenticationService, LoginData
from services.user import UserService


def render_register_user() -> ServiceResponse:
    questions = [
        Text("email", "Enter your email"),
        Text("password", "Enter your password"),
    ]
    answers = cast(dict[str, str], prompt(questions))
    email = answers["email"]
    password = answers["password"]

    response = AuthenticationService().register_user(email, password)
    return response


def render_login_user() -> ServiceResponse:
    questions = [
        Text("email", "Enter your email"),
        Text("password", "Enter your password"),
    ]
    answers = cast(dict[str, str], prompt(questions))
    email = answers["email"]
    password = answers["password"]

    info = get_user_meta_data()
    login_location = info["country"]
    login_device = info["location"]

    meta_data = LoginData(
        login_location=getattr(Country, login_location.upper(), Country.SOUTH_AFRICA),
        login_device=login_device,
        login_method=LoginMethod.EMAIL,
    )
    response = AuthenticationService().login_user(email, password, meta_data)
    return response


def get_user_meta_data() -> dict[str, str]:
    ip_info = requests.get("https://ipinfo.io/json").json()
    result = {
        "region": ip_info.get("region"),
        "country": ip_info.get("country"),
        "city": ip_info.get("city"),
    }
    return {
        "location": ", ".join([value for value in result.values() if value]),
        "ip": ip_info.get("ip", "0.0.0.0"),
        "country": (ip_info.get("timezone") or "South Africa").split("/")[-1],
    }


def handle_intro(answers: dict[str, str]) -> ServiceResponse:
    match answers["intro"]:
        case "Register User":
            return render_register_user()
        case "Login User":
            return render_login_user()
        case "Exit":
            return ServiceResponse(
                message="Exit Application.",
                status=ServiceStatus.INFO,
                data={"exit": True},
            )
        case _:
            raise ValueError("Invalid option selected.")


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

            if response.status == ServiceStatus.SUCCESS:
                if answers["intro"] == "Register User":
                    print("[🔐] User registered successfully.")
                    continue

                if (
                    not response.data
                    or "id" not in response.data
                    or "token" not in response.data
                ):
                    print("[❌] User ID/Token not found.")
                    continue

                print(f"[🔐] User ID: {response.data['id']}")
                user_id = response.data["id"]
                token = response.data["token"]
                continue

        services = [
            List(
                "services",
                "Select a service",
                choices=["User", "Block Chain"],
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
                        # "Manage Account",
                        # "View Account",
                        # "Add Payment Profile",
                    ],
                )
            ]
            answer = cast(dict[str, str], prompt(user_services))
            if answer["user_services"] == "Create Account":
                print(f"[{user_id} 🔐] Create Account Service Selected.")
                response = UserService().create_user_account(str(user_id))
                print(
                    f"Response: {response.message} | Status: {response.status} | Data: {response.data}"
                )
                if response.status != ServiceStatus.SUCCESS:
                    print("[❌] Failed to create user account.")

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


if __name__ == "__main__":
    main()
