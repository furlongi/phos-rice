import json
import subprocess
import sys
from typing import List


class WorkspaceSwitcher:
    # Configure this based on your monitor
    def monitor_spaces(self, focused_workspace) -> int:
        match focused_workspace:
            case "DP-1":
                return [4, 5, 6, 7]
            case "DP-2":
                return [3, 8]
            case "DP-3":
                return [2]
            case _:
                return 1

    def single_monitor_spaces(self) -> int:
        return [1, 2, 3, 4]

    def __init__(self, direction, is_single_device=False, is_window_mode=False):
        self.direction = direction
        self.is_single_device = is_single_device
        self.is_window_mode = is_window_mode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="WorkspaceSwitcher",
        description="Manages switching between workspaces when multiple monitors exist",
    )

    parser.add_argument("direction")
    parser.add_argument("-s", "--single", action="store_true")
    parser.add_argument("-w", "--window", action="store_true")

    args = parser.parse_args()

    direction = args.direction
    is_single_device = args.single
    is_window_mode = args.window

    SyncConfigs(
        verbose=is_verbose, is_push=is_push, slow=is_slow, device_type=device_type
    ).sync_files()


#########################


cli_args = sys.argv

# scriptname
# direction [left] [right]
# type [move] next ws, [container] move to next ws
# monitormode [single] [multi]
if len(cli_args) != 4:
    print("Not all args given")
    raise SystemExit


direction = -1 if cli_args[1] == "left" else 1  # right
move_type = cli_args[2]  # move / container
monitormode = cli_args[3]  # single / multi


# Get Current Workspace info and load
workspaces = subprocess.check_output(["swaymsg", "-t", "get_workspaces"], text=True)
parsed_workspaces = json.loads(workspaces)


# Get available workspaces for monitor
focused_workspace = [i for i in parsed_workspaces if i["focused"]][0]
focused_workspace_num = focused_workspace["num"]
focused_workspace_name = focused_workspace["output"]
if monitormode == "single":
    avail_workspaces: list = single_monitor_spaces()
else:
    avail_workspaces: list = monitor_spaces(focused_workspace_name)


# Pick the next available slot
next_workspace = None
if focused_workspace_num not in avail_workspaces:
    # Created a workspace out of limits, go back
    next_workspace = avail_workspaces[0]
else:
    index = avail_workspaces.index(focused_workspace_num)
    index += direction
    if index < 0:
        next_workspace = avail_workspaces[-1]
    else:
        next_workspace = avail_workspaces[index % len(avail_workspaces)]


# Launch script
if move_type == "test":
    print(
        f"Next: {next_workspace}; Monitor: {focused_workspace_name}; Avail: {avail_workspaces}"
    )
elif move_type == "move":
    subprocess.call(["swaymsg", "workspace", "number", str(next_workspace)])
elif move_type == "container":
    subprocess.call(
        [
            "swaymsg",
            "move",
            "container",
            "to",
            "workspace",
            str(next_workspace),
            "," "workspace",
            "number",
            str(next_workspace),
        ]
    )
else:
    print("Invalid Command")
