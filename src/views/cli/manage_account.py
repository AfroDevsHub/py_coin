from typing import Any, Type, cast
from uuid import UUID

from inquirer import List, Text, prompt
from pydantic import BaseModel
from src.models.user.accounts import Account
from src.services.user import UserService
from src.lib.types.services.user import UserUpdateData
from src.lib.types.user.accounts import UpdateAccountData
from src.lib.types.user.payments import UpdatePaymentProfileData
from src.lib.types.user.profiles import UpdateUserProfileData
from src.lib.types.user.settings import UpdateSettingsProfileData


def display_manage_account_sections(account: Account) -> None:
    update_data = UserUpdateData()
    account_updates_data = UpdateAccountData()
    payment_updates_data = UpdatePaymentProfileData()
    user_updates_data = UpdateUserProfileData()
    settings_updates_data = UpdateSettingsProfileData()

    while True:
        sections = [
            List(
                "section",
                f"[{account.id}] Select a Section",
                choices=[
                    "Update Account",
                    "Update Payment Profile",
                    "Update User Profile",
                    "Update Settings",
                    "Back",
                ],
            )
        ]
        section = cast(dict[str, str], prompt(sections))

        match section["section"]:
            case "Update Account":
                print(f"[✏️] Updating account {account.id}.")
                field = handle_input_choices(UpdateAccountData.model_fields)

                value = handle_matched_input(UpdateAccountData, field)
                setattr(account_updates_data, field, value)
                print(f"Account {account.id} updated with {field} = {value}.")

            case "Update Payment Profile":
                print(f"[✏️] Updating payment profile for account {account.id}.")
                field = handle_input_choices(UpdatePaymentProfileData.model_fields)

                value = handle_matched_input(UpdatePaymentProfileData, field)
                setattr(payment_updates_data, field, value)
                print(f"Account {account.id} updated with {field} = {value}.")

            case "Update User Profile":
                print(f"[✏️] Updating user profile for account {account.id}.")
                field = handle_input_choices(UpdateUserProfileData.model_fields)

                value = handle_matched_input(UpdateUserProfileData, field)
                setattr(user_updates_data, field, value)
                print(f"Account {account.id} updated with {field} = {value}.")

            case "Update Settings":
                print(f"[✏️] Updating settings for account {account.id}.")
                field = handle_input_choices(UpdateSettingsProfileData.model_fields)

                value = handle_matched_input(UpdateSettingsProfileData, field)
                setattr(settings_updates_data, field, value)
                print(f"Account {account.id} updated with {field} = {value}.")

            case "Back":
                print("[🔙] Going back to the previous menu.")
                break
            case _:
                break
    update_data.account = account_updates_data
    update_data.profile = user_updates_data
    update_data.settings = settings_updates_data
    update_data.payments = payment_updates_data

    UserService().update_user_account(cast(UUID, account.id), update_data)


def handle_input_choices(model: dict[str, Any]):
    account_updates = [
        List(
            "field",
            "Select a field to update",
            choices=[field for field in model],
        )
    ]
    field = cast(dict[str, str], prompt(account_updates))["field"]
    print(f"Selected field to update: {field}")

    return field


def handle_matched_input(model: Type[BaseModel], field: str) -> Any:
    schema = model().model_json_schema()
    prompts = [handle_new_value_input(schema, field)]

    value = cast(
        dict[str, str],
        prompt(prompts),
    )

    return resolve_enum_from_value(model, field, value["value"])


def resolve_enum_from_value(model: Type[BaseModel], field: str, value: str) -> Any:
    from importlib import import_module

    field_type = model.model_fields[field].annotation
    type_str = str(field_type)
    # Split on " | " to handle Union types
    type_names = [t.strip() for t in type_str.split(" | ")]
    if type_names[0] == "bool":
        print(field)
        return (
            True
            if value.lower().strip().startswith("t") or value.lower().strip().startswith("y")
            else False
        )

    for type_name in type_names:
        # Only process if it's an Enum type (contains a dot and not 'None' or 'str')
        if "." in type_name and "None" not in type_name and "str" not in type_name:
            # Dynamically import the Enum class
            module_path, class_name = type_name.rsplit(".", 1)
            try:
                enum_class = getattr(import_module(module_path), class_name)
                if issubclass(enum_class, Enum):
                    for member in enum_class:
                        if member.value == value or member.name == value:
                            return member
            except Exception:
                continue
    return value


def handle_new_value_input(schema: dict[str, Any], field: str) -> List | Text:
    fields = schema["properties"][field]

    if "$ref" in fields or ("anyOf" in fields and "$ref" in fields["anyOf"][0]):
        return List(
            "value",
            f"Enter new value for {field}",
            choices=(
                [
                    value
                    for key, value in schema["$defs"][field.title()].items()
                    if key in "enum"
                ][0]
            ),
        )

    return Text("value", f"Please Enter New {field.title()} Value")
