import json

from phoscli.utils.term import process, process_fixed, process_read

_HYPR = "hyprctl"


def active_workspace() -> dict[str, str]:
    out = _hyprwrapper_read("activeworkspace -j")
    return json.loads(out)


def switch_workspace(workspace_name: int, monitor: str) -> str:
    args: dict[str, str | int] = {"workspace": workspace_name}
    return _hyprwrapper_disp("focus", args)


def move_to_workspace(workspace_name: int, monitor: str) -> str:
    args: dict[str, str | int] = {"workspace": workspace_name, "follow": "true"}
    return _hyprwrapper_disp("window.move", args)


# Deprecated potentially since hy3 depends on this
def move_to_monitor(monitor_name: str) -> str:
    return _hyprwrapper_disp(f"movewindow mon:{monitor_name}")


def _hyprwrapper(arg: str) -> str:
    return process(f"{_HYPR} {arg}")[1]


def _hyprwrapper_disp(command: str, arg: dict[str, str | int]) -> str:
    return process_fixed(_HYPR, "dispatch", f"hl.dsp.{command}({_parse_args(arg)})")[1]


def _hyprwrapper_read(arg: str) -> str:
    return process_read(f"{_HYPR} {arg}")[1]


def _parse_args(args: dict[str, str | int]) -> str:
    if len(args) < 1:
        return ""

    result = "{"
    for key, val in args.items():
        result += f'{key}="{val}",'

    return result.strip(",") + "}"
