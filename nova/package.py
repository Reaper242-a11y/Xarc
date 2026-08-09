import json
import tarfile
from pathlib import Path


FORMAT_VERSION = 1


class NovaPackage:
    def __init__(self, path):
        self.path = Path(path)
        self.manifest = None

    def read_manifest(self):
        if not self.path.exists():
            raise FileNotFoundError(
                f"Package not found: {self.path}"
            )

        if not self.path.is_file():
            raise ValueError(
                f"Not a file: {self.path}"
            )

        try:
            with tarfile.open(self.path, "r:*") as archive:

                try:
                    manifest_file = archive.extractfile(
                        "manifest.json"
                    )
                except KeyError:
                    manifest_file = None

                if manifest_file is None:
                    raise ValueError(
                        "manifest.json is missing"
                    )

                self.manifest = json.load(
                    manifest_file
                )

        except tarfile.TarError as error:
            raise ValueError(
                f"Invalid Nova package: {error}"
            )

        self.validate()

        return self.manifest

    def validate(self):
        if not isinstance(self.manifest, dict):
            raise ValueError(
                "Package manifest must be an object"
            )

        required = [
            "format",
            "name",
            "version",
            "architecture",
            "description",
            "license"
        ]

        for field in required:
            if field not in self.manifest:
                raise ValueError(
                    f"Manifest missing required field: {field}"
                )

        if self.manifest["format"] != FORMAT_VERSION:
            raise ValueError(
                f"Unsupported Nova package format: "
                f"{self.manifest['format']}"
            )

        if not self.manifest["name"]:
            raise ValueError(
                "Package name cannot be empty"
            )

        if not self.manifest["version"]:
            raise ValueError(
                "Package version cannot be empty"
            )

        if not isinstance(
            self.manifest.get("dependencies", []),
            list
        ):
            raise ValueError(
                "dependencies must be a list"
            )

    def info(self):
        if self.manifest is None:
            self.read_manifest()

        return self.manifest
