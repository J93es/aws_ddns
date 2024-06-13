import os, json
import src.aws_ddns_start

import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

config_path = os.path.dirname(os.path.abspath(__file__)) + "/config.json"
with open(config_path) as fs:
    aws_ddns_config = json.load(fs)
