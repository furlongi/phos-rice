import argparse
import os
from shutil import copy2, copytree
from time import sleep
from typing import Any, Dict, List, Tuple

from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    Task,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)

HOME = os.path.expanduser("~")
CONF_PATH = os.path.join(HOME, ".config")

DEVICE_CONF = "custom_device.conf"


class CustomBarColumn(BarColumn):
    def __init__(self, *args, **kwargs):
        super().__init__(
            bar_width=40,
            style="white",
        )

    def render(self, task: Task):
        barcolor = task.fields.get("mcolor", "white")
        finish_color = task.fields.get("mfinish", "green1")
        self.complete_style = f"{barcolor} on {barcolor}"
        self.finished_style = f"{finish_color}"
        return super().render(task)


class SyncConfigs:
    def __init__(self, verbose=False, is_push=True, slow=False, device_type="desktop"):
        self.verbose: bool = verbose
        self.is_push: bool = is_push
        self.slow: bool = slow
        self.device_type: str = device_type

    def sync_files(self):
        with Progress(
            SpinnerColumn(spinner_name="arc"),
            TextColumn("[progress.description]{task.description}"),
            CustomBarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>1.0f}%"),
            TimeElapsedColumn(),
        ) as progress:
            # List out the dot files to copy here
            params = [
                # NAME, TEXT COLOR, BAR COLOR
                ("hypr", "blue", {"ignore_files": ["device"]}),
                ("swaync", "yellow", {}),
                ("fish", "cyan", {}),
                ("kitty", "red", {"ignore_files": ["kitty.conf.bak"]}),
                ("ags", "blue", {"ignore_hidden": True}),
            ]

            single_files = ["libinput-gestures.conf"]

            mainTask = progress.add_task(
                "[red]Copying Configs...",
                total=len(params),
                mcolor="red",
            )

            # To sort the progress bars, for the main task at the bottom
            def order_renderables(this):
                tasks = this.tasks
                table = this.make_tasks_table(
                    sorted(tasks, reverse=True, key=lambda x: x.id)
                )
                yield table

            progress.get_renderables = order_renderables.__get__(progress)

            # Copy the files
            for service, color, configs in params:
                path = os.path.join(CONF_PATH, service)
                count = self.list_files(path, configs)
                colorname = "blue" if color is None else color

                task = progress.add_task(
                    f"[{colorname}]Copying {service}...",
                    total=len(count),
                    mcolor=colorname,
                )

                self.sync(path, service, progress, task, configs)
                progress.update(mainTask, advance=1)

            task = progress.add_task(
                f"[white]Copying Singular files...",
                total=len(single_files),
                mcolor="white",
            )
            self.sync_singles(single_files, CONF_PATH, progress, task)

    def sync(
        self,
        conf_path: str,
        conf_name: str,
        progress: Progress,
        task: TaskID,
        configs: Dict[str, Any],
    ) -> None:
        dot_path = f"./.config/{conf_name}"
        source_path, destin_path = self.direction(conf_path, dot_path)

        source_files = self.list_files(source_path, configs)
        destin_files = self.list_files(destin_path, configs)

        self.handle_deletions(source_files, destin_files, conf_name, destin_path)

        for folder, file in source_files:
            if self.slow:
                sleep(0.2)
            print(f"[{conf_name}] Copying {source_path}/{folder}/{file}")

            self.copy(source_path, folder, file, conf_name, destin_path)

            progress.update(task, advance=1)

        self.handle_device_config(conf_path, conf_name, progress, task)

    def sync_singles(
        self, target_files: List[str], conf_path: str, progress: Progress, task: TaskID
    ):
        dot_path = f"./.config"
        source_path, destin_path = self.direction(conf_path, dot_path)

        for file in target_files:
            src_path = f"{source_path}/{file}"
            dst_path = f"{destin_path}/"

            if self.verbose:
                print(f"---- [FILE] {source_path}/{file} -> {destin_path}/{file}")

            copy2(src_path, dst_path)
            progress.update(task, advance=1)

    def copy(
        self,
        source_path: str,
        folder_name: str,
        source_file: str,
        conf_name: str,
        destin_path: str,
    ):
        src = f"{source_path}/{folder_name}/{source_file}"
        dst = f"{destin_path}/{folder_name}"
        dstf = f"{dst}/{source_file}"

        if self.verbose:
            print(f"---- [{conf_name}] {src} -> {dst}")

        if not os.path.exists(dst):
            os.makedirs(dst, exist_ok=True)

        copy2(src, dst)

    def list_files(
        self, target_path: str, configs: Dict[str, Any]
    ) -> List[Tuple[str, str]]:
        files: List[Tuple[str, str]] = []
        ignore_files = set(configs.get("ignore_files", []))
        ignore_files = ignore_files.union({DEVICE_CONF})

        ignore_hidden = configs.get("ignore_hidden", False)

        for path, i, filenames in os.walk(target_path):
            folder_name = path.split(target_path)[-1].strip("/")
            if (ignore_hidden and len(folder_name) > 0 and folder_name[0] == ".") or (
                folder_name in ignore_files
            ):
                continue

            for file in filenames:
                if (ignore_hidden and len(file) > 0 and file[0] == ".") or (
                    file in ignore_files
                ):
                    continue

                files.append((folder_name, file))
        return files

    # -> src, dst
    def direction(self, conf_path: str, local_path: str) -> Tuple[str, str]:
        if self.is_push:
            return local_path, conf_path
        return conf_path, local_path

    def handle_device_config(
        self, conf_path: str, conf_name: str, progress: Progress, task: TaskID
    ):
        source, destin = self.direction(
            f"{conf_path}/{DEVICE_CONF}",
            f"./.config/{conf_name}/device/{device_type}.conf",
        )

        if os.path.isfile(source):
            if not self.is_push and not os.path.exists(
                f"./.config/{conf_name}/device/"
            ):
                os.makedirs(f"./.config/{conf_name}/device/", exist_ok=True)

            copy2(source, destin)

            progress.update(task, advance=1)
            if self.verbose:
                print(f"+[{conf_name}] {source} -> {destin}")
            if self.slow:
                sleep(0.1)

    def handle_deletions(
        self,
        source_files: List[Tuple[str, str]],
        destin_files: List[Tuple[str, str]],
        conf_name: str,
        destin_path: str,
    ):
        hashed_sources = {file for _, file in source_files}

        missing_files = []
        for folder, file in destin_files:
            if file not in hashed_sources:
                missing_files.append(destin_path + "/" + folder + "/" + file)

        for file in missing_files:
            print(f"==== [{conf_name}] Removing {file}")
            os.remove(file)


# https://rich.readthedocs.io/en/stable/reference/progress.html#rich.progress.Progress
# https://docs.python.org/3/library/argparse.html
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ConfigCopier",
        description="Copies the config dot files to and from .config to the gihub folder",
    )

    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-p", "--push", action="store_true")
    parser.add_argument("-s", "--slow", action="store_true")
    parser.add_argument("-d", "--dry", action="store_true")
    parser.add_argument("--device")

    args = parser.parse_args()

    is_verbose = args.verbose
    is_push = args.push
    is_slow = args.slow
    dry_run = args.dry
    device_type = args.device or "desktop"

    SyncConfigs(
        verbose=is_verbose,
        is_push=is_push,
        slow=is_slow,
        device_type=device_type,
    ).sync_files()
