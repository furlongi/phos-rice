import subprocess


def process(args: str) -> int:
    proc_args = args.split(" ")
    return subprocess.call(proc_args)


def process_read(args: str) -> str:
    proc_args = args.split(" ")
    return subprocess.check_output(proc_args, text=True)
