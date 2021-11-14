import json
import os


class ExtensionFunction:
    @staticmethod
    def getJsonFILE(path: str) -> json:
        cur_path = os.path.dirname(__file__)

        relative_path = os.path.relpath(path, cur_path)

        print(relative_path)

        file = open(relative_path)

        return json.load(file)
