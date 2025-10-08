import importlib
import os
from typing import Any


from models.model import BaseModel


class DatabaseCheckController:
    folder = "models"

    def __init__(self):
        pass

    def test_models(self, models: list[dict[str, BaseModel]]) -> dict[str, Any]:
        result = {}
        for model in models:
            result |= {
                key: self.__test_connection(value) for key, value in model.items()
            }

        return result

    def get_models(self) -> list[dict[str, Any]]:
        result = []
        for folder in self.__get_folders():
            result.extend(self.__get_modules(folder))
        return result

    def __test_connection(self, model: BaseModel) -> str:
        if model().test():
            return "ACTIVE"
        return "INACTIVE"

    def __get_folders(self) -> list[str]:
        return [
            folder
            for folder in os.listdir("models")
            if not folder.endswith(".py") and not folder.startswith("__")
        ]

    def __get_modules(self, folder: str) -> list[dict[str, Any]]:
        return [
            self.__get_model(f"models.{folder}.{module.rstrip('.py')}")
            for module in os.listdir(f"models/{folder}")
            if not module.startswith("__")
        ]

    def __get_model(self, module) -> dict[str, Any]:
        response = importlib.import_module(module)
        return {
            key: value
            for key, value in response.__dict__.items()
            if "<class 'models." in str(value) and key != "BaseModel"
        }
