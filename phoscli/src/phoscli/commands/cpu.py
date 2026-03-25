from argparse import Namespace
from typing import List, Dict
from phoscli.utils.stats import cpu_usage_percent

class Cpu:
    def __init__(self, args: Namespace):
        super()

    def run(self):
        result = cpu_usage_percent()
        if result is None:
            print("null")
            return "null"
        print(result)
        return result