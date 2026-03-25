from phoscli.utils.term import process, process_read
from typing import Dict, Optional
import json
import re

def get_current_device_alias(current_device: str) -> Optional[str]:
    devices = process_read("ratbagctl list")[1]
    for dev in devices.split("\n"):
        alias, device = dev.split(":")
        if current_device in device:
            return alias.strip()
    
    return None

def set_profile(device_alias: str, profile_name: str) -> (bool, str):
    status, result = process_read(f"ratbagctl {device_alias} profile active set {profile_name}")
    if status == 0:
        return True, ""
    return False, result
    


