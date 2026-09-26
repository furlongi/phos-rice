from typing import cast

from .customtyping import DOT_TYPE


class Config:
    def __init__(self, dot_settings: DOT_TYPE, single_settings: dict[str, list[str]]):
        self._config: DOT_TYPE = dot_settings
        self._single: dict[str, list[str]] = single_settings

    def __len__(self):
        return len(self._config)

    @property
    def color(self) -> str:
        return cast(str, self._config.get("color", "blue"))

    def services(self):
        for k in self._config.keys():
            yield k

    def get_color(self, key: str) -> str:
        default = "blue"
        mapping = self._config.get(key, None)
        if mapping is None:
            return default

        return cast(str, mapping.get("color", default))

    def get_custom_files(self, key: str) -> list[str]:
        default: list[str] = []
        mapping = self._config.get(key, None)
        if mapping is None:
            return default

        return cast(list[str], mapping.get("custom_files", default))

    def get_custom_files_set(self, key: str) -> set[str]:
        return set(self.get_custom_files(key))

    def get_custom_folders(self, key: str) -> list[str]:
        default: list[str] = []
        mapping = self._config.get(key, None)
        if mapping is None:
            return default

        return cast(list[str], mapping.get("custom_folders", default))

    def get_custom_folders_set(self, key: str) -> set[str]:
        return set(self.get_custom_folders(key))

    def get_ignore_files(self, key: str) -> list[str]:
        default: list[str] = []
        mapping = self._config.get(key, None)
        if mapping is None:
            return default

        return cast(list[str], mapping.get("ignore_files", default))

    def get_ignore_files_set(self, key: str) -> set[str]:
        return set(self.get_ignore_files(key))

    def get_ignore_folders(self, key: str) -> list[str]:
        default: list[str] = []
        mapping = self._config.get(key, None)
        if mapping is None:
            return default

        return cast(list[str], mapping.get("ignore_folders", default))

    def get_ignore_folders_set(self, key: str) -> set[str]:
        return set(self.get_ignore_folders(key))

    def do_ignore_hidden(self, key: str) -> bool:
        default = False
        mapping = self._config.get(key, None)
        if mapping is None:
            return default

        return cast(bool, mapping.get("ignore_hidden", default))

    def get_single_files(self):
        return self._single.get("single", [])

    def get_single_custom_files(self):
        return self._single.get("custom", [])
