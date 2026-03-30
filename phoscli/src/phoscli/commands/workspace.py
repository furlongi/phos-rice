from argparse import Namespace
from typing import Dict, List

from phoscli.utils.hypr import active_workspace, move_to_workspace, switch_workspace


class Workspace:
    args: Namespace
    direction: int
    is_single_screen: bool
    is_window_mode: bool
    is_test: bool

    def monitor_spaces(self, focused_workspace) -> List[int]:
        match focused_workspace:
            case "DP-1":
                return [1, 2, 3, 4]
            case "DP-2":
                return [5, 6]
            case "DP-3":
                return [7, 8]
            case "eDP-1":
                return [1, 2, 3, 4, 5]
            case _:
                return [9]

    def single_monitor_spaces(self) -> List[int]:
        return [1, 2, 3, 4, 5]

    def __init__(self, args: Namespace):
        self.args = args
        direction = self.args.direction[0]

        if direction in ["r", "1"]:
            self.direction = 1
        elif direction in ["l", "-1"]:
            self.direction = -1
        else:
            raise ValueError(f"Invalid direction {self.args.direction}")

        self.is_single_screen = self.args.single
        self.is_window_mode = self.args.window
        self.is_test = self.args.test

    def run(self):
        workspace_info = active_workspace()
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
            move_to_workspace(next_workspace)
        else:
            switch_workspace(next_workspace)
