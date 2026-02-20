import json
import subprocess
import sys
from typing import List, Dict
import argparse


class WorkspaceSwitcher:
    # Configure this based on your monitor
    def monitor_spaces(self, focused_workspace) -> [int]:
        match focused_workspace:
            case "DP-1":
                return [1, 5, 6, 7]
            case "DP-2":
                return [2, 8]
            case "DP-3":
                return [3, 9]
            case _:
                return [4]

    def single_monitor_spaces(self) -> int:
        return [1, 2, 3, 4]

    def __init__(
        self, direction, is_single_screen=False, is_window_mode=False, is_test=False
    ):
        self.direction = direction
        self.is_single_screen = is_single_screen
        self.is_window_mode = is_window_mode
        self.is_test = is_test

    def get_workspace(self) -> Dict[str, str]:
        workspaces = subprocess.check_output(
            ["hyprctl", "activeworkspace", "-j"], text=True
        )
        return json.loads(workspaces)

    def dispatch(self):
        workspace_info = self.get_workspace()
        focused = workspace_info["monitor"]
        focused_workspace_num = workspace_info["id"]

        if self.is_single_screen:
            avail_workspaces: list = self.single_monitor_spaces()
        else:
            avail_workspaces: list = self.monitor_spaces(focused)

        if focused_workspace_num not in avail_workspaces:
            # Currently inside a workspace out of limits, go back
            next_workspace = avail_workspaces[0]
        else:
            index = avail_workspaces.index(focused_workspace_num)
            index += self.direction
            if index < 0:
                next_workspace = avail_workspaces[-1]
            else:
                next_workspace = avail_workspaces[index % len(avail_workspaces)]

        # Launch script
        if self.is_test:
            print(
                f"Next: {next_workspace}; Monitor: {focused}; Cur: {focused_workspace_num}; Avail: {avail_workspaces}"
            )
        elif self.is_window_mode:
            subprocess.call(
                [
                    "hyprctl",
                    "dispatch",
                    "movetoworkspace",
                    str(next_workspace),
                ]
            )
        else:
            subprocess.call(["hyprctl", "dispatch", "workspace", str(next_workspace)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="WorkspaceSwitcher",
        description="Manages switching between workspaces when multiple monitors exist",
    )

    parser.add_argument("direction")
    parser.add_argument("-s", "--single", action="store_true", default=False)
    parser.add_argument("-w", "--window", action="store_true", default=False)
    parser.add_argument("-t", "--test", action="store_true", default=False)

    args = parser.parse_args()

    direction = int(args.direction)
    is_single_screen = args.single
    is_window_mode = args.window
    is_test = args.test

    WorkspaceSwitcher(
        direction=direction,
        is_single_screen=is_single_screen,
        is_window_mode=is_window_mode,
        is_test=is_test,
    ).dispatch()
