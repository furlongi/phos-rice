from phoscli.utils.term import process, process_read, process_pipes
from typing import Dict
import json
import re

def cpu_usage_percent() -> int:
    # Returns usage as a percentage
    free_cpu = process_pipes("top -bn1 | grep \"Cpu(s)\" | sed \"s/.*, *\\([0-9.]*\\)%* id.*/\\1/\"")
    if free_cpu is None:
        return None

    return round(100 - float(free_cpu), 1)

def ram_usage_percent() -> int:
    ram_usage = process_pipes("free | grep Mem | awk '{print $3/$2 * 100.0}'")
    if ram_usage is None or len(ram_usage) < 1:
        return None
    return round(float(ram_usage), 1)