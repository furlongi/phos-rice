from argparse import Namespace
from typing import List, Dict
from phoscli.utils.hypr import active_workspace, move_to_monitor


class Tiling:
    args: Namespace
    direction: int

    def adjacent_monitor(self, focused_monitor) -> [str]:
        match focused_monitor:
            case "DP-1":
                return ["DP-3", "DP-2"]
            case "DP-2":
                return ["DP-1", None]
            case "DP-3":
                return ["HDMI-A-1", "DP-1"]
            case _:
                return [None, "DP-3"]

    def __init__(self, args: Namespace):
        direction = args.direction[0]

        if direction in ["r", "1"]:
            self.direction = 1
        elif direction in ["l", "-1"]:
            self.direction = 0
        else:
            raise ValueError(f"Invalid direction {self.args.direction}")

    def run(self):
        workspace_info = active_workspace()
        focused = workspace_info["monitor"]

        adjacents = self.adjacent_monitor(focused)

        next_monitor = adjacents[self.direction]
        if next_monitor is None:
            return  # No adjacent monitor / No wrapping

        move_to_monitor(next_monitor)
