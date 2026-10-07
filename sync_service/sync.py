import os
from shutil import copy2
from time import sleep

from rich.progress import Progress

from .customtyping import FileList


class Sync:

    def __init__(
        self,
        config_path: str,
        local_path: str,
        custom_path: str,
        progress: Progress,
        is_push: bool,
        is_slow: bool,
        dry_run: bool,
        verbose: bool,
    ):
        self.config_path: str = config_path
        self.local_path: str = local_path
        self.custom_path: str = custom_path

        self.progress: Progress = progress
        self.is_push: bool = is_push
        self.is_slow: bool = is_slow
        self.dry_run: bool = dry_run
        self.verbose: bool = verbose

    class SyncUnit:
        def __init__(
            self,
            sync_instance: Sync,
            service: str,
            color: str,
            is_custom: bool,
            task_name: str,
        ):
            self.sync_instance: Sync = sync_instance
            self.service: str = service
            self.color: str = color
            self.is_custom: bool = is_custom
            self.task_name: str = task_name

            self.destination_path: str = ""
            self.destination_files: FileList = []
            self.source_path: str = ""
            self.source_files: FileList = []

        def _set_destination(self, destin_path: str, destin_files: FileList):
            self.destination_path = destin_path
            self.destination_files = destin_files

        def _set_source(self, source_path: str, source_files: FileList):
            self.source_path = source_path
            self.source_files = source_files

        def write(self):
            if len(self.source_files) < 1:
                print(self._log(f"Skipping writes, {self.source_path} is empty."))
                return

            task = self.sync_instance.progress.add_task(
                self._taskdesc(),
                total=len(self.source_files),
                mcolor=self.color,
            )

            for folder, file in self.source_files:
                if self.sync_instance.is_slow:
                    sleep(0.2)
                print(
                    self._log(
                        f"Copying {self.source_path}/{self.service}/{folder}/{file.strip("/")}"
                    )
                )

                self._copy(
                    self.source_path, folder, file, self.service, self.destination_path
                )
                self.sync_instance.progress.update(task, advance=1)

        def delete(self):
            # If local is missing, skip deletes (everything already gone)
            if len(self.source_path) < 1:
                print(self._log(f"Skipping delete, {self.source_path} empty."))
                return

            hashed_sources = {f"{folder}/{file}" for folder, file in self.source_files}

            missing_files: list[str] = []
            for folder, file in self.destination_files:
                if f"{folder}/{file}" not in hashed_sources:
                    missing_files.append(
                        f"{self.destination_path}/{self.service}/{folder}/{file}"
                    )

            for file in missing_files:
                if self.sync_instance.is_slow:
                    sleep(0.2)
                print(f"==== [{self.service}] Removing {file}")

                if not self.sync_instance.dry_run:
                    os.remove(file)

        def single_writes(self):
            if len(self.source_files) < 1:
                print(self._log("Skipping single writes, no files found."))
                return

            task = self.sync_instance.progress.add_task(
                self._taskdesc(),
                total=len(self.source_files),
                mcolor=self.color,
            )

            for _, file in self.source_files:
                src_path = f"{self.source_path}/{file}"
                dst_path = f"{self.destination_path}/"

                if self.sync_instance.verbose:
                    print(f"---- [FILE] {src_path} -> {dst_path}/{file}")

                if not self.sync_instance.dry_run:
                    _ = copy2(src_path, dst_path)
                self.sync_instance.progress.update(task, advance=1)

        def single_deletes(self):
            hashed_sources = {file for _, file in self.source_files}
            missing_files: list[str] = []

            for _, file in self.destination_files:
                if file not in hashed_sources:
                    missing_files.append(file)

            for file in missing_files:
                if self.sync_instance.is_slow:
                    sleep(0.2)
                print(self._log(f"==== [FILE] Removing {file}"))
                file_path = f"{self.destination_path}/{file}"

                if not self.sync_instance.dry_run:
                    os.remove(file_path)

        def _copy(
            self,
            source_path: str,
            folder_name: str,
            source_file: str,
            conf_name: str,
            destin_path: str,
        ):
            src = f"{source_path}/{self.service}/{folder_name}/{source_file}"
            dst = f"{destin_path}/{self.service}/{folder_name}"

            if self.sync_instance.verbose:
                print(f"---- [{conf_name}] {src} -> {dst}")

            if not self.sync_instance.dry_run:
                if not os.path.exists(dst):
                    os.makedirs(dst, exist_ok=True)

                _ = copy2(src, dst)

        def _log(self, message: str):
            return f"[{self.service}] {"(CUSTOM)" if self.is_custom else ""} {message}"

        def _taskdesc(self):
            return f"[{self.color}]Copying {self.task_name}{" (CUSTOM)" if self.is_custom else ""}..."

    # Factor a SyncUnit using the relevant data for a service
    def load_syncer(
        self,
        service: str,
        conf_files: FileList,
        local_files: FileList,
        color: str,
        is_custom: bool = False,
        task_name: str = "",
    ):
        sync_unit = self.SyncUnit(self, service, color, is_custom, task_name)

        origin_path = self.custom_path if is_custom else self.local_path

        # Sort the direction of where the files will go
        if self.is_push:
            source_path = origin_path
            destin_path = self.config_path

            source_list = local_files
            destin_list = conf_files
        else:
            source_path = self.config_path
            destin_path = origin_path

            source_list = conf_files
            destin_list = local_files

        sync_unit._set_destination(  # pyright: ignore[reportPrivateUsage]
            destin_path, destin_list
        )
        sync_unit._set_source(  # pyright: ignore[reportPrivateUsage]
            source_path, source_list
        )

        return sync_unit
