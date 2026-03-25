import json
import os
from typing import Dict, Optional

_LOCAL_PATH = "/phoscli/configs/"

def load_config(file_name) -> Optional[Dict]:
    try:
        with open(os.getcwd() + _LOCAL_PATH + file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Let command handle error
        return None