import subprocess
from typing import List


def process(args: str) -> (int, str):
    try:
        proc_args = args.split(" ")
        return subprocess.call(proc_args), ""
    except subprocess.CalledProcessError as E:
        return 1, "Execution Error"

def process_read(args: str) -> (int, str):
    proc_args = args.split(" ")
    try:
        return 0, subprocess.check_output(proc_args, text=True)
    except subprocess.CalledProcessError as E:
        return 1, E.output.strip()

def process_pipes(args: List[str]) -> str:
    p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)

    return p.stdout.read().decode('utf-8')
