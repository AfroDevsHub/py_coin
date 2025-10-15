import json
import os
from typing import Any


class VersionCheckController:
    def __init__(self):
        pass

    def confirm_version(self) -> dict[str, Any]:
        result = {}
        for line in self.__read_file():
            parts = line.split("=")
            if len(parts) == 2:
                result[parts[0].strip().lower()] = json.loads(parts[1].strip())
        return result

    def __read_file(self) -> list[str]:
        try:
            print(os.listdir())
            with open("version.py", "r") as file:
                return file.readlines()
        except BaseException as e:
            print(e)
            return []
