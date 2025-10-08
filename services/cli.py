"""Services: CLI Service."""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from enum import Enum
from json import dumps, loads
import json
import sys
import textwrap
from types import UnionType
from typing import Any, Type, Union, get_type_hints
from uuid import UUID
from pyinputplus import (
    inputMenu,
    inputStr,
    inputBool,
    inputFloat,
    inputInt,
    inputYesNo,
    inputDate,
)
from datetime import datetime


from lib.exceptions import ApplicationError, CLIError
from lib.types.blockchain import ContractData, TransactionData
from lib.types.cli import Args
from lib.types.user import AccountData, Logindata, ProfileData, SettingsData, UserData
from lib.utils.constants.users import SocialMediaLink
from lib.utils.encryption.cryptography import decrypt_data
from services.blockchain import BlockChainService
from services.authentication import AuthenticationService
from services.user import UserService


class Cli:
    """Manages CLI Operations."""

    ACTIVE = True
    __FORMATTER__ = RawDescriptionHelpFormatter
    __EPILOG__ = "\n"  # "🪙   New Age BlockChain Services. 🪙"
    __PROLOG__ = """
🚀  Welcome to the Block Type CLI! 🌟

🔹  Explore the Power of PYCoin  🔹

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                      ┃
┃  Simplifying smart transacting and contracting.      ┃
┃  Unlock the potential of effortless block chaining!  ┃
┃                                                      ┃
┃  📈  Seamless integration with your workflows        ┃
┃  💡  Intelligent options tailored just for you       ┃
┃  🌐  Global reach, local convenience                 ┃
┃                                                      ┃
┃  Go ahead, let's shape the future of transactions    ┃
┃  and contracts together!                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
    __INSTANCE__ = None
    __GENERAL_ARGS__ = {
        "create": {"args": ("create",), "kwargs": {"help": "Creates Resource."}},
        "read": {"args": ("read",), "kwargs": {"help": "Gets Resource."}},
        "update": {"args": ("update",), "kwargs": {"help": "Updates Resource."}},
        "help": {"args": ("help",), "kwargs": {"help": "Help Information."}},
    }
    __TRANSACTION_ARGS__ = {
        "transaction": {
            "args": ("--transaction", "-T"),
            "kwargs": {
                "action": "store_true",
                "help": "Create a Transaction.",
            },
        }
    }
    __CONTRACT_ARGS__ = {
        "contract": {
            "args": ("--contract", "-C"),
            "kwargs": {
                "action": "store_true",
                "help": "Create a Contract.",
            },
        }
    }
    __BLOCK_ARGS__ = {
        "block": {
            "args": ("--block", "-B"),
            "kwargs": {
                "action": "store_true",
                "help": "Create a block.",
            },
        },
    }

    __USER_ARGS__ = {
        "user": {
            "args": ("--user", "-U"),
            "kwargs": {
                "action": "store_true",
                "help": "Create a User.",
            },
        }
    }

    __DATA_ARGS__ = {
        "model_id": {
            "args": ("--uuid", "-id"),
            "kwargs": {
                "help": "Model ID.",
            },
        },
        "sender": {
            "args": ("--sender", "-s"),
            "kwargs": {
                "help": "Sender/Contractor's ID.",
            },
        },
        "receiver": {
            "args": ("--receiver", "-r"),
            "kwargs": {
                "help": "Receiver/Contractee's ID.",
            },
        },
        "sender_signiture": {
            "args": ("--sender-signiture", "-ss"),
            "kwargs": {
                "help": "Sender/Contractor's Signiture ID.",
            },
        },
        "receiver_signiture": {
            "args": ("--receiver-signiture", "-rs"),
            "kwargs": {
                "help": "Receiver/Contractee's Signiture ID.",
            },
        },
        "data": {
            "args": ("--data", "-d"),
            "kwargs": {
                "action": "store_true",
                "help": "Add Model Data.",
            },
        },
    }

    def __new__(cls) -> "Cli":
        """Singleton Class Constructor."""

        if cls.__INSTANCE__:
            return cls.__INSTANCE__

        cls.parser = ArgumentParser(
            formatter_class=cls.__FORMATTER__,
            epilog=textwrap.dedent(cls.__EPILOG__),
            description=textwrap.dedent(cls.__PROLOG__),
        )
        cls.__set_cli_help__()
        cls.__set_cli_args__()
        cls.__INSTANCE__ = super().__new__(cls)
        print(f"{Cli.__PROLOG__}{Cli.__EPILOG__}CLI App started. Type 'exit' to quit.")
        return cls.__INSTANCE__

    @classmethod
    def __set_cli_help__(cls):
        cls.subparsers = cls.parser.add_subparsers(
            dest="command", required=True, help="Sub-command help"
        )

    @classmethod
    def __set_cli_args__(cls):
        # Add subparsers for general commands
        for command, command_args in cls.__GENERAL_ARGS__.items():
            subparser = cls.subparsers.add_parser(
                command, help=command_args["kwargs"]["help"]
            )
            cls.__add_args__(subparser, cls.__TRANSACTION_ARGS__)
            cls.__add_args__(subparser, cls.__CONTRACT_ARGS__)
            cls.__add_args__(subparser, cls.__BLOCK_ARGS__)
            cls.__add_args__(subparser, cls.__USER_ARGS__)
            cls.__add_args__(subparser, cls.__DATA_ARGS__)

    @classmethod
    def args_parser(cls, args: Args) -> dict[str, Any]:
        required_options = {
            "transaction": args.transaction,
            "contract": args.contract,
            "user": args.user,
            "block": args.block,
        }
        data = [key for key, arg in required_options.items() if arg]

        if len(data) != 1:
            return "Invalid Command - Try *help*"

        match (args.command):
            case "create":
                if args.transaction:
                    arg_data = cls.__get_arg_data__("transaction")
                    return (
                        BlockChainService()
                        .create_transaction(
                            UUID(args.sender),
                            UUID(args.receiver),
                            float(arg_data["amount"]),
                        )
                        .to_dict()
                    )
                if args.contract:
                    arg_data = cls.__get_arg_data__("contract")
                    with open(arg_data["contract"], "r") as file:
                        return (
                            BlockChainService()
                            .create_contract(
                                UUID(args.sender), UUID(args.receiver), file.read()
                            )
                            .to_dict()
                        )
                if args.user:
                    arg_data = cls.__get_arg_data__("user")
                    response = AuthenticationService().register_user(
                        arg_data["email"], arg_data["password"]
                    )
                    user = json.loads(decrypt_data(response.data.get("user")))
                    proceed = inputYesNo(
                        "Create a User Profile? (Yes/No): ", default="yes"
                    )
                    profiles = ["profile", "account", "settings"]

                    if proceed == "no":
                        return response.message

                    data = {}
                    for profile in profiles:
                        arg_data = cls.__get_arg_data__(profile)
                        data[profile] = arg_data

                    user_profile = UserService().create_user_account(
                        UUID(user["id"]), data
                    )

                    return user_profile
                    # return user.to_dict()
                    # account = UserService().create_user_account(user.)
            case "update":
                if args.transaction:
                    return (
                        BlockChainService()
                        .update_transaction(
                            args.uuid,
                            args.sender_signiture,
                            args.receiver_signiture,
                            arg_data,
                        )
                        .to_dict()
                    )
                if args.contract:
                    return (
                        BlockChainService()
                        .update_contract(
                            args.uuid,
                            args.sender_signiture,
                            args.receiver_signiture,
                            arg_data,
                        )
                        .to_dict()
                    )
                if args.block:
                    return BlockChainService().append_block_chain(args.uuid).to_dict()

                # if args.user:
                #     return UserService().create_user_account()
            case "read":
                if args.user:
                    return (
                        AuthenticationService()
                        .login_user(
                            arg_data["email"],
                            arg_data["password"],
                            UserData(login=arg_data),
                        )
                        .to_dict()
                    )
        return "Invalid Command - Try *help*"

    @classmethod
    def run(cls) -> None:
        while True:
            try:
                # Capture input from standard input
                if cls.ACTIVE:
                    command = input("iPYCoin: ")
                    if command == "help":
                        print(cls.help())
                        continue

                    if command == "kill":
                        cls.kill()
                        break

                    # Parse the input command and handle it
                    args = cls.parser.parse_args(command.split())
                    parsed_args = cls.args_parser(args)
                    print(parsed_args)
            except (KeyboardInterrupt, CLIError):
                raise CLIError("CLI Server Was Terminated.")
            except (SystemExit, EOFError, ApplicationError) as e:
                print(e)
                continue

    @classmethod
    def kill(cls) -> None:
        print("PYCoin CLI Terminated.")
        cls.ACTIVE = False

    @classmethod
    def help(cls) -> str:
        cls.parser.print_help()
        result = []
        args = {
            "Transaction": {**cls.__TRANSACTION_ARGS__, **cls.__DATA_ARGS__},
            "Contract": {**cls.__CONTRACT_ARGS__, **cls.__DATA_ARGS__},
            "Block": {
                **cls.__BLOCK_ARGS__,
                **{
                    "model_id": cls.__DATA_ARGS__["model_id"],
                    "data": cls.__DATA_ARGS__["data"],
                },
            },
            "User": {
                **cls.__USER_ARGS__,
                **{
                    "model_id": cls.__DATA_ARGS__["model_id"],
                    "data": cls.__DATA_ARGS__["data"],
                },
            },
        }
        for key, value in args.items():
            result.append(f"\n{key}:")

            # Calculate maximum lengths
            max_arg_0_length = max(len(arg["args"][0]) for arg in value.values()) + 1
            max_arg_1_length = max(len(arg["args"][1]) for arg in value.values()) + 1

            for kwarg, arg in value.items():
                arg_0 = arg["args"][0]
                arg_1 = arg["args"][1]
                arg_help = arg["kwargs"]["help"]
                result.append(
                    f"  {arg_0:<{max_arg_0_length}} {arg_1:<{max_arg_1_length}} {arg_help}"
                )

        return (
            "\n".join(result)
            + "\n\nExamples:\n  create -T -d\n  read -T\n  create -U -email ##### -p #####\n  create -C --sender-signature ##### --receiver-signature #####\n"
        )

    @staticmethod
    def __add_args__(subparser: ArgumentParser, args: dict[str, Any]) -> None:
        """Add Subparser's Args for Help Page."""
        for _, arg in args.items():
            subparser.add_argument(*arg["args"], **arg["kwargs"])

    @staticmethod
    def __get_arg_data__(model: str) -> dict[str, Any]:
        models = {
            "user": Logindata,
            "profile": ProfileData,
            "account": AccountData,
            "settings": SettingsData,
            "contract": ContractData,
            "transaction": TransactionData,
        }
        data = {}

        for key, annotation in get_type_hints(models[model]).items():
            while True:
                try:
                    response = Cli.get_input_for_annotation(key, annotation)
                    data[key] = response
                    break
                except ValueError as e:
                    print(f"Invalid input for {key} (expected {annotation}): {e}")
        return data

    @staticmethod
    def get_input_for_annotation(field_name: str, annotation: Any) -> Any:
        models = {
            "user": UserData,
            "profile": ProfileData,
            "account": AccountData,
            "settings": SettingsData,
            "contract": ContractData,
            "transaction": TransactionData,
        }

        origin = getattr(annotation, "__origin__", None)
        if (isinstance(annotation, UnionType) or origin is Union) and type(
            None
        ) in annotation.__args__:
            annotation = annotation.__args__[0]  # Get the type inside Optional

        if annotation in models.values():
            for key, value in models.items():
                print(annotation, models.values(), value, key)
                if value == annotation:
                    return Cli.__get_arg_data__(key)
            raise CLIError("Invalid Annotation.")

        if origin is list:
            item_type = annotation.__args__[0]
            list_items = []
            while True:
                input_value = inputStr(
                    f"Enter a value for {field_name.title().replace("_", " ")} (leave empty to finish): ",
                    blank=True,
                )
                if input_value == "":
                    break
                list_items.append(Cli.get_input_for_annotation(field_name, item_type))
            return list_items

        if origin is dict:
            _, value_type = annotation.__args__
            dict_items = {}
            while True:
                key_input = inputStr(
                    f"Enter a key for {field_name.title().replace("_", " ")} (leave empty to finish): ",
                    blank=True,
                )
                if key_input == "":
                    break
                value_input = Cli.get_input_for_annotation(field_name, value_type)
                dict_items[key_input] = value_input
            return dict_items

        if isinstance(annotation, type) and issubclass(annotation, Enum):
            if annotation is SocialMediaLink:
                input_dict = {}
                while True:
                    platform = inputMenu(
                        [e.name for e in SocialMediaLink],
                        prompt="Choose a Social Media Platform:\n",
                        numbered=True,
                        blank=True,
                    )
                    link = inputStr(f"Enter URL for {platform}: ")
                    input_dict[platform] = link
                    more = inputYesNo(
                        "Add another social media link? (yes/no): ", blank=True
                    )
                    if more.lower() != "yes":
                        break
                return input_dict
            response = inputMenu(
                [dumps(e.value) for e in annotation],
                prompt=f"{field_name.title().replace("_", " ")}:\n",
                numbered=True,
                blank=True,
            )
            if response:
                return loads(response)
            return None

        response = None
        if annotation is int:
            response = inputInt(f"{field_name.title().replace("_", " ")}: ", blank=True)
        elif annotation is float:
            response = inputFloat(
                f"{field_name.title().replace("_", " ")}: ", blank=True
            )
        elif annotation is bool:
            response = inputBool(
                f"{field_name.title().replace("_", " ")}: ", blank=True
            )
        elif annotation is str:
            response = inputStr(f"{field_name.title().replace("_", " ")}: ", blank=True)
        elif annotation is datetime:
            response = inputDate(
                f"{field_name.title().replace("_", " ")} (dd/mm/yyyy): ",
                formats=["%d/%M/%Y"],
                blank=True,
            )
        elif hasattr(annotation, "__annotations__"):
            nested_data = {}
            print(f"Enter values for {field_name.title().replace("_", " ")}:")
            for nested_key, nested_type in get_type_hints(annotation).items():
                nested_data[nested_key] = Cli.get_input_for_annotation(
                    nested_key, nested_type
                )
            response = nested_data
        else:
            raise ValueError(f"Unsupported type: {annotation}")

        if not response:
            return None
        return response
