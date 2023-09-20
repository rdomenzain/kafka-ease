import os
import json

from click import echo
import yaml


class ReadFile:
    def __init__(self, filename):
        self.filename = filename

    def read(self) -> dict:
        """Read a file and return the content
        Returns:
            dict: Content of the file
        """
        try:
            if not os.path.exists(self.filename):
                raise ValueError(f"File {self.filename} does not exists")

            if self.filename.endswith(".json"):
                echo("JSON file detected")
                with open(self.filename, "r") as f:
                    data = json.load(f)
            elif self.filename.endswith(".yaml") or self.filename.endswith(
                ".yml"
            ):
                echo("YAML file detected")
                with open(self.filename, "r") as f:
                    data = yaml.safe_load(f)
            else:
                raise ValueError(
                    "File extension not supported (only .json and .yaml/.yml"
                )

            return data
        except Exception as e:
            raise ValueError(f"Error reading file {self.filename}: {e}")
