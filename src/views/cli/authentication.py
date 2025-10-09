from typing import cast
from inquirer import Text, prompt
import requests

from lib.interfaces.responses import ServiceResponse
from lib.utils.constants.responses import ServiceStatus
from lib.utils.constants.users import Country, LoginMethod
from services.authentication import AuthenticationService, LoginData


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


def get_user_meta_data(ip: str | None = None) -> dict[str, str]:
    if ip:
        ip_info = requests.get(f"https://ipinfo.io/{ip}/json").json()
    else:
        ip_info = requests.get(f"https://ipinfo.io/json").json()
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
