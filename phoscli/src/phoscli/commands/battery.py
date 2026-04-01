from argparse import Namespace
from typing import List, Dict
from phoscli.utils.stats import battery_usage_stats
import json

class Battery:
    def __init__(self, args: Namespace):
        super()

    def run(self):
        result = battery_usage_stats()
        if result is None:
            print("null")
            return "null"
        json_result = json.dumps(result)
        print(json_result)
        return json_result