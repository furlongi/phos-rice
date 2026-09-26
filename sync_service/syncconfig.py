import os
from typing import cast

from boltons.iterutils import is_collection
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from .config import Config
from .custombars import CustomBarColumn
from .customtyping import DOT_TYPE
from .sync import Sync

HOME = os.path.expanduser("~")
CONF_PATH = os.path.join(HOME, ".config")
LOCAL_PATH = f"./.config"
LOCAL_CUSTOM_PATH = f"./.custom_config"


class SyncConfigs:
    def __init__(
        self,
        dot_settings: DOT_TYPE,
        single_files: dict[str, list[str]],
        verbose: bool = False,
        is_push: bool = True,
        slow: bool = False,
        dry_run: bool = False,
        device_type: str = "desktop",
    ):
        self.config_map: Config = Config(dot_settings, single_files)
        self.verbose: bool = verbose
        self.is_push: bool = is_push
        self.is_slow: bool = slow
        self.dry_run: bool = dry_run
        self.device_type: str = device_type

    def sync_files(
        self,
    ):
        with Progress(
            SpinnerColumn(spinner_name="arc"),
            TextColumn("[progress.description]{task.description}"),
            CustomBarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>1.0f}%"),
            TimeElapsedColumn(),
        ) as progress:

            # Setup the progress
            mainTask = progress.add_task(
                "[red]Copying Configs...",
                total=len(self.config_map),
                mcolor="red",
            )

            # Func to sort the progress bars, for the main task at the bottom
            def order_renderables(this):  # pyright: ignore[reportUnknownParameterType]
                tasks = this.tasks  # pyright: ignore[reportUnknownVariableType]
                table = (  # pyright: ignore[reportUnknownVariableType]
                    this.make_tasks_table(
                        sorted(
                            tasks,  # pyright: ignore[reportUnknownArgumentType]
                            reverse=True,
                            key=lambda x: cast(
                                int, x.id  # pyright: ignore[reportUnknownArgumentType]
                            ),
                        )
                    )
                )
                yield table

            progress.get_renderables = order_renderables.__get__(progress)

            local_custom_path = os.path.join(LOCAL_CUSTOM_PATH, self.device_type)
            sync_manager = Sync(
                config_path=CONF_PATH,
                local_path=LOCAL_PATH,
                custom_path=local_custom_path,
                progress=progress,
                is_push=self.is_push,
                is_slow=self.is_slow,
                dry_run=self.dry_run,
                verbose=self.verbose,
            )

            ### Process Service Files ###

            # Start the sync for each service
            for service in self.config_map.services():
                _custom_files = self.config_map.get_custom_files_set(service)
                _custom_folders = self.config_map.get_custom_folders_set(service)
                _ignore_files = self.config_map.get_ignore_files_set(service)
                _ignore_folders = self.config_map.get_ignore_files_set(service)
                _do_ignore_hidden = self.config_map.do_ignore_hidden(service)
                _color = self.config_map.get_color(service)

                # Find local files
                conf_path = os.path.join(CONF_PATH, service)
                conf_files, conf_cust_files = self.list_conf_files(
                    target_path=conf_path,
                    custom_folders=_custom_folders,
                    custom_files=_custom_files,
                    ignore_folders=_ignore_folders,
                    ignore_files=_ignore_files,
                    do_ignore_hidden=_do_ignore_hidden,
                )

                # Find local staging configs
                local_path = os.path.join(LOCAL_PATH, service)
                local_custom_path_service = os.path.join(local_custom_path, service)
                local_files, local_cust_files = self.list_local_files(
                    target_path=local_path,
                    local_custom_path=local_custom_path_service,
                    ignore_folders=_ignore_folders,
                    ignore_files=_ignore_files,
                    do_ignore_hidden=_do_ignore_hidden,
                )

                # Load SyncUnit for regular sync
                sync_unit = sync_manager.load_syncer(
                    service, conf_files, local_files, _color, task_name=service
                )

                # Process deletes then writes
                sync_unit.delete()
                sync_unit.write()

                # Process custom writes
                sync_unit = sync_manager.load_syncer(
                    service,
                    conf_cust_files,
                    local_cust_files,
                    _color,
                    is_custom=True,
                    task_name=service,
                )
                sync_unit.delete()
                sync_unit.write()

                # Update main task
                progress.update(mainTask, advance=1)

            ### Process Single Files ###

            # Start the sync for single files
            conf_sf, conf_cust_sf = self.list_conf_single_files(
                CONF_PATH,
                self.config_map.get_single_files(),
                self.config_map.get_single_custom_files(),
            )

            local_sf, local_cust_sf = self.list_local_single_files(
                CONF_PATH,
                LOCAL_CUSTOM_PATH,
                self.config_map.get_single_files(),
                self.config_map.get_single_custom_files(),
            )

            # Process regular files
            sync_unit = sync_manager.load_syncer(
                "", conf_sf, local_sf, "white", task_name="Single"
            )
            sync_unit.single_deletes()
            sync_unit.single_writes()

            # Process custom files
            sync_unit = sync_manager.load_syncer(
                "",
                conf_cust_sf,
                local_cust_sf,
                "white",
                is_custom=True,
                task_name="Single",
            )
            sync_unit.single_deletes()
            sync_unit.single_writes()

    def list_conf_files(
        self,
        target_path: str,
        custom_folders: set[str] = set(),
        custom_files: set[str] = set(),
        ignore_folders: set[str] = set(),
        ignore_files: set[str] = set(),
        do_ignore_hidden: bool = False,
    ) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
        found_files: list[tuple[str, str]] = []
        custom_instances: list[tuple[str, str]] = []

        for folder_name, file in self._filesystem_walk(
            target_path, ignore_folders, ignore_files, do_ignore_hidden
        ):
            if folder_name in custom_folders or file in custom_files:
                custom_instances.append((folder_name, file))
            else:
                found_files.append((folder_name, file))

        return found_files, custom_instances

    def list_local_files(
        self,
        target_path: str,
        local_custom_path: str,
        ignore_folders: set[str] = set(),
        ignore_files: set[str] = set(),
        do_ignore_hidden: bool = False,
    ):

        found_files: list[tuple[str, str]] = []
        custom_instances: list[tuple[str, str]] = []

        for folder_name, file in self._filesystem_walk(
            target_path, ignore_folders, ignore_files, do_ignore_hidden
        ):
            found_files.append((folder_name, file))

        for folder_name, file in self._filesystem_walk(
            local_custom_path, ignore_folders, ignore_files, do_ignore_hidden
        ):
            custom_instances.append((folder_name, file))

        return found_files, custom_instances

    def list_conf_single_files(
        self,
        target_path: str,
        expected_files: list[str] = list(),
        custom_files: list[str] = list(),
    ) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
        found_files: list[tuple[str, str]] = []
        custom_instances: list[tuple[str, str]] = []

        for file in self._surface_file_walk(target_path, expected_files):
            found_files.append((target_path, file))

        for file in self._surface_file_walk(target_path, custom_files):
            custom_instances.append((target_path, file))

        return found_files, custom_instances

    def list_local_single_files(
        self,
        target_path: str,
        custom_path: str,
        expected_files: list[str] = list(),
        custom_files: list[str] = list(),
    ) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
        found_files: list[tuple[str, str]] = []
        custom_instances: list[tuple[str, str]] = []

        for file in self._surface_file_walk(target_path, expected_files):
            found_files.append((target_path, file))

        for file in self._surface_file_walk(custom_path, custom_files):
            custom_instances.append((custom_path, file))

        return found_files, custom_instances

    def _filesystem_walk(
        self,
        target_path: str,
        ignore_folders: set[str] = set(),
        ignore_files: set[str] = set(),
        do_ignore_hidden: bool = False,
    ):
        for path, _, filenames in os.walk(target_path):
            folder_name = path.split(target_path)[-1].strip("/")

            if self._should_ignore_hidden(
                do_ignore_hidden, folder_name, ignore_folders
            ):
                continue

            for file in filenames:
                if self._should_ignore_hidden(do_ignore_hidden, file, ignore_files):
                    continue

                yield (folder_name, file)

    def _surface_file_walk(self, target_path: str, expected_files: list[str]):
        for file in expected_files:
            if os.path.isfile(os.path.join(target_path, file)):
                yield file

    def _should_ignore_hidden(
        self, ignore_hidden: bool, entity_name: str, ignore_list: set[str]
    ):
        if (ignore_hidden and len(entity_name) > 0 and entity_name[0] == ".") or (
            entity_name in ignore_list
        ):
            return True
