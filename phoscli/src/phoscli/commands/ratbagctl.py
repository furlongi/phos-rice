from argparse import Namespace
from typing import List, Dict, Optional
from phoscli.utils.ratbagcli import get_current_device_alias, set_profile
from phoscli.utils.config import load_config
from glom import glom

_CONFIG_NAME = "mouse_profiles.json"

class RatBagCtl:
    args: Namespace
    profile: str
    device: Optional[str]

    def __init__(self, args: Namespace):
        self.args = args
        self.profile = args.profile[0]
        self.device = args.device

    def run(self):
        configs = load_config(_CONFIG_NAME)
        if configs is None:
            print("No mouse_profile.json found!")
            return

        current_device = self.device if self.device is not None else configs["default_target"]
        target_profile = glom(configs, f"{current_device}.{self.profile}.profile")
        if target_profile is None:
            print(f"Profile {self.profile} not found for device {current_device}!")
            return None

        device_alias = get_current_device_alias(current_device)

        if device_alias is None:
            print(f"Device {current_device} is not  connected!")
            return

        status, message = set_profile(device_alias, target_profile)
        if not status:
            print("Failed to set profile:", message)

