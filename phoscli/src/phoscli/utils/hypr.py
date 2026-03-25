from phoscli.utils.term import process, process_read
from typing import Dict
import json

_HYPR = "hyprctl"


def active_workspace() -> Dict:
    out = _hyprwrapper_read("activeworkspace -j")
    return json.loads(out)


def switch_workspace(workspace_name: str) -> (int, str):
    return _hyprwrapper_disp(f"workspace {workspace_name}")


def move_to_workspace(workspace_name: str) -> (int, str):
    return _hyprwrapper_disp(f"movetoworkspace {workspace_name}")


def move_to_monitor(monitor_name: str) -> (int, str):
    return _hyprwrapper_disp(f"movewindow mon:{monitor_name}")


def _hyprwrapper(arg: str) -> str:
    return process(f"{_HYPR} {arg}")[1]


def _hyprwrapper_disp(arg: str) -> str:
    return process(f"{_HYPR} dispatch {arg}")[1]


def _hyprwrapper_read(arg: str) -> str:
    return process_read(f"{_HYPR} {arg}")[1]
