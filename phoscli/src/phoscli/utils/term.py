import subprocess
from typing import List


def process(args: str) -> tuple[int, str]:
    print(">", args)
    try:
        proc_args = args.split(" ")
        return subprocess.run(proc_args), ""
    except subprocess.CalledProcessError as E:
        return 1, "Execution Error"


def process_fixed(base_cmd: str, act_cmd: str, args: str) -> tuple[int, str]:
    try:
        return subprocess.call([base_cmd, act_cmd, args]), ""
    except subprocess.CalledProcessError as _:
        return 1, "Execution Error"


def process_read(args: str) -> tuple[int, str]:
    proc_args = args.split(" ")
    try:
        return 0, subprocess.check_output(proc_args, text=True)
    except subprocess.CalledProcessError as E:
        return 1, E.output.strip()


def process_pipes(args: List[str]) -> str:
    p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)

    return p.stdout.read().decode("utf-8")
