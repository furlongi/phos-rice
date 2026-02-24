import argparse
import os
from shutil import copy2, copytree
from time import sleep

from blueman.main.PulseAudioUtils import ArgumentError
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
                ("hypr", "blue"),
                ("swaync", "yellow"),
                ("fish", "cyan"),
                ("kitty", "red"),
            ]

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
            for service, color in params:
                path = os.path.join(CONF_PATH, service)
                count = self.count_files(path)
                colorname = "blue" if color is None else color

                task = progress.add_task(
                    f"[{colorname}]Copying {service}...", total=count, mcolor=colorname
                )

                self.copy_with_progress(path, service, progress, task)
                progress.update(mainTask, advance=1)

    def copy_with_progress(
        self, conf_path: str, conf_name: str, progress: Progress, task: TaskID
    ) -> None:
        def copy_file_with_progress(src: str, dst: str, *args):
            progress.update(task, advance=1)
            if self.verbose:
                print(f"---- [{conf_name}] {src} -> {dst}")
            if self.slow:
                sleep(0.1)
            return copy2(src, dst)

        def ignore_and_log(path: str, names: str):
            # This gets called for every folder.
            # Using it as a logger
            if self.slow:
                sleep(0.2)
            print(f"[{conf_name}] Copying {path}")
            return [DEVICE_CONF, "/device/*"]  # Ignore these files

        source, destin = self.direction(conf_path, f"./.config/{conf_name}/")

        copytree(
            source,
            destin,
            ignore=ignore_and_log,
            copy_function=copy_file_with_progress,
            dirs_exist_ok=True,
        )

        self.handle_device_config(conf_path, conf_name, progress, task)

    def count_files(self, path: str) -> int:
        total = 0
        for _, _, filenames in os.walk(path):
            total += len(filenames)
        if self.verbose:
            print(f"Total files for {path}: {total}")
        return total

    # -> src, dst
    def direction(self, conf_path: str, local_path: str):
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
    parser.add_argument("--device")

    args = parser.parse_args()

    is_verbose = args.verbose
    is_push = args.push
    is_slow = args.slow
    device_type = args.device or "desktop"

    SyncConfigs(
        verbose=is_verbose, is_push=is_push, slow=is_slow, device_type=device_type
    ).sync_files()
