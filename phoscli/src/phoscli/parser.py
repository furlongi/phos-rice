import argparse
from phoscli.commands import workspace, tiling, cpu, ram, ratbagctl


def parse() -> str:
    parser = argparse.ArgumentParser(
        prog="phoscli", description="Main control script for hypr phos"
    )

    parser.add_argument(
        "-v", "--version", action="store_true", help="Print the current version"
    )

    # Subcommand
    subparser = parser.add_subparsers(
        title="Subcommands",
        description="Available subcommands",
        metavar="COMMANDS",
    )

    # Workspaces
    workspace_parser = subparser.add_parser("workspace", help="Manage hypr workspace")
    workspace_parser.set_defaults(command=workspace.Workspace)
    workspace_parser.add_argument(
        "direction",
        nargs=1,
        choices=["1", "-1", "l", "r"],
        help="The direction to move left or right to the next workspace",
    )
    workspace_parser.add_argument(
        "-s",
        "--single",
        action="store_true",
        help="Workspace rules for single monitor setup",
    )
    workspace_parser.add_argument(
        "-w",
        "--window",
        action="store_true",
        help="If moving a window with the workspace",
    )
    workspace_parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Used for debugging, prints an test output",
    )

    # Tiling
    tiling_parser = subparser.add_parser(
        "tiling", help="Workaround for hy3 multi monitor"
    )
    tiling_parser.set_defaults(command=tiling.Tiling)
    tiling_parser.add_argument(
        "direction",
        nargs=1,
        choices=["1", "-1", "l", "r"],
        help="The direction to move left or right to the next workspace",
    )

    ### Integrations
    # CPU Usage
    cpu_parser = subparser.add_parser(
        "cpu", help="Returns CPU usage",
    )
    cpu_parser.set_defaults(command=cpu.Cpu)

    ram_parser = subparser.add_parser(
        "ram", help="Returns Ram usage",
    )
    ram_parser.set_defaults(command=ram.Ram)

    # ratbagctl
    rat_parser = subparser.add_parser(
        "ratbagctl",
        aliases=["rat", "mouse"],
        help="Sets gaming mouse profile"
    )
    rat_parser.add_argument(
        "profile",
        nargs=1
    )
    rat_parser.add_argument(
        "-d",
        "--device",
    )
    rat_parser.set_defaults(command=ratbagctl.RatBagCtl)

    return parser, parser.parse_args()
