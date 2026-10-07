import argparse
from typing import cast

from sync_service import syncconfig

# List out the dot files to copy here
DOT_SETTINGS: dict[
    str, dict[str, str | list[str]] | dict[str, str] | dict[str, str | bool]
] = {
    "hypr": {
        "color": "blue",
        "custom_files": ["custom_device.lua"],
        "custom_folders": ["custom_device"],
    },
    "fish": {"color": "cyan"},
    "kitty": {"color": "red", "ignore_files": ["kitty.conf.bak"]},
    "noctalia": {
        "color": "purple",
        "ignore_files": ["private.toml"],
        "custom_files": ["custom.toml"],
    },
}

SINGLE_FILES: dict[str, list[str]] = {
    "single": [],
    "custom": ["libinput-gestures.conf"],
}


# https://rich.readthedocs.io/en/stable/reference/progress.html#rich.progress.Progress
# https://docs.python.org/3/library/argparse.html
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ConfigCopier",
        description="Copies the config dot files to and from .config to the gihub folder",
    )

    _ = parser.add_argument("-v", "--verbose", action="store_true")
    _ = parser.add_argument("-p", "--push", action="store_true")
    _ = parser.add_argument("-s", "--slow", action="store_true")
    _ = parser.add_argument("-d", "--dry", action="store_true")
    _ = parser.add_argument("--device")

    args = parser.parse_args()

    is_verbose = cast(bool, args.verbose)
    is_push = cast(bool, args.push)
    is_slow = cast(bool, args.slow)
    dry_run = cast(bool, args.dry)
    device_type = cast(str, args.device) or "desktop"

    syncconfig.SyncConfigs(
        dot_settings=DOT_SETTINGS,
        single_files=SINGLE_FILES,
        verbose=is_verbose,
        is_push=is_push,
        slow=is_slow,
        dry_run=dry_run,
        device_type=device_type,
    ).sync_files()
