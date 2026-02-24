import argparse
from phoscli.commands import workspace, tiling


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

    # Triling
    workspace_parser = subparser.add_parser(
        "tiling", help="Workaround for hy3 multi monitor"
    )
    workspace_parser.set_defaults(command=tiling.Tiling)
    workspace_parser.add_argument(
        "direction",
        nargs=1,
        choices=["1", "-1", "l", "r"],
        help="The direction to move left or right to the next workspace",
    )

    return parser, parser.parse_args()
