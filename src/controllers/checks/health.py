import importlib
import os
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy import Boolean, Select, cast

from src.models import ENGINE


class DatabaseCheckController:
    folder = "models"

    def test_models(self, models: list[dict[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for model in models:
            result |= {
                key: self.__test_connection(value) for key, value in model.items()
            }

        return result

    def get_models(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for folder in self.__get_folders():
            modules = self.__get_modules(folder)
            result.extend(modules)
        return result
    
    def __test_model(self, model: Any) -> bool:
        try:
            with Session(ENGINE) as session:
                data = Select(model).where(cast(1 == 1, Boolean))
                session.execute(data)
            return True
        except BaseException as e:
            print(e)
            return False


    def __test_connection(self, model: Any) -> str:
        if self.__test_model(model):
            return "ACTIVE"
        return "INACTIVE"

    def __get_folders(self) -> list[str]:
        return [
            folder
            for folder in os.listdir(f"./{self.folder}")
            if not folder.endswith(".py") and not folder.startswith("__")
        ]

    def __get_modules(self, folder: str) -> list[dict[str, Any]]:
        return [
            self.__get_model(f"src.models.{folder}.{module.rstrip('.py')}")
            for module in os.listdir(f"./{self.folder}/{folder}")
            if not module.startswith("__")
        ]

    def __get_model(self, module: str) -> dict[str, Any]:
        response = importlib.import_module(module)
        return {
            key: value
            for key, value in response.__dict__.items()
            if "<class 'src.models." in str(value) and key != "BaseModel"
        }
