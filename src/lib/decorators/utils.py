"""Decorators: Utility Wrapper Functions."""

from enum import Enum
from functools import wraps
from typing import (
    Tuple,
    get_type_hints,
    List,
    Dict,
    Any,
    Union,
    get_origin,
    get_args,
)

from src.lib.types.exceptions import ApplicationError



def validate_function_signature(is_method: bool = False):
    """Validates wrapped functions and methods' type hints."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            hints = get_type_hints(func)
            if is_method and args:
                _validate_args(*args[1:], hints=hints)
            else:
                _validate_args(*args, hints=hints)
            _validate_kwargs(hints, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def _validate_args(*args, hints: dict[str, Any]):
    """Validates positional arguments."""

    for index, arg in enumerate(args):
        if index >= len(hints):
            raise ApplicationError("Too many arguments provided.")
        param_name = list(hints.keys())[index]
        expected_type = hints[param_name]
        if not check_type(arg, expected_type):
            raise ApplicationError(
                f"Invalid Argument for '{param_name}'. "
                + f"Expected {expected_type} but got {type(arg)}."
            )


def _validate_kwargs(hints: dict[str, Any], **kwargs):
    """Validates key-word arguments."""

    for key, value in kwargs.items():
        if key not in hints:
            raise ApplicationError(f"Unexpected keyword argument '{key}'.")
        expected_type = hints[key]
        if not check_type(value, expected_type):
            raise ApplicationError(
                f"Invalid Keyword Argument for '{key}'. "
                + f"Expected {expected_type} but got {type(value)}."
            )


def check_type(value: Any, expected_type: Any) -> bool:
    """Check if the value matches the expected type, including nested and complex types."""

    origin = get_origin(expected_type)
    args = get_args(expected_type)
    if origin is Union:
        return any(check_type(value, t) for t in args if t is not type(None)) or (
            value is None and type(None) in args
        )

    if isinstance(expected_type, type) and isinstance(value, expected_type):
        return True

    if origin is Enum:
        return isinstance(value, expected_type)

    if origin in (list, List, tuple, Tuple):
        return __check_list__(args, value)

    if origin in (dict, Dict):
        return __check_dict__(args, value)

    if hasattr(expected_type, "__annotations__") and isinstance(expected_type, type):
        return __check_complex_type__(args, value)

    if isinstance(value, bool) and expected_type is int:
        return False

    return isinstance(value, expected_type) or value is value


def __check_list__(args: Tuple[Any], value: list) -> bool:
    """Checks Args of Type List."""

    if not isinstance(value, (list, tuple)):
        return False
    item_type = args[0]
    return all(check_type(item, item_type) for item in value)


def __check_dict__(args: Tuple[Any, Any], value: dict) -> bool:
    if not isinstance(value, dict):
        return False
    key_type, val_type = args
    return all(check_type(k, key_type) for k in value.keys()) and all(
        check_type(v, val_type) for v in value.values()
    )


def __check_complex_type__(expected_type: Any, value: Any) -> bool:
    if not isinstance(value, dict) and isinstance(value, expected_type):
        return True

    if not isinstance(value, dict):
        return False

    if isinstance(value, expected_type):
        return True

    try:
        for key, key_type in expected_type.__annotations__.items():
            if key not in value or not check_type(value[key], key_type):
                return False
    except AttributeError as e:
        print(e)
    return True
