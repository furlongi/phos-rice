from argparse import Namespace
from typing import List, Dict
from phoscli.utils.stats import ram_usage_percent

class Ram:
    def __init__(self, args: Namespace):
        super()

    def run(self):
        result = ram_usage_percent()
        if result is None:
            print("null")
            return "null"
        print(result)
        return result