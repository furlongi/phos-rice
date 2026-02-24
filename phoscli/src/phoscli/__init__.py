from phoscli.parser import parse

# from phoscli.utils.version import print_version


def main() -> None:
    parser, args = parse()
    if args.version:
        # print_version()
        raise NotImplementedError
    elif "command" in args:
        args.command(args).run()
    else:
        parser.print_help()
