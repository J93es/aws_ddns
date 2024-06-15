import os, json

try:
    config_path = os.path.dirname(os.path.abspath(__file__)) + r"/../config.json"
    with open(config_path) as fs:
        aws_ddns_config = json.load(fs)
except Exception as e:
    print(f'Failed to open config.json: {e}')
    exit(1)

try:
    if "USE_DISCORD" not in aws_ddns_config:
        raise Exception("USE_DISCORD is not in config.json")
    if "AWS_ACCESS_KEY_ID" not in aws_ddns_config:
        raise Exception("AWS_ACCESS_KEY_ID is not in config.json")
    if "AWS_SECRET_ACCESS_KEY" not in aws_ddns_config:
        raise Exception("AWS_SECRET_ACCESS_KEY is not in config.json")
    if "HostedZones" not in aws_ddns_config:
        raise Exception("HostedZones is not in config.json")

    USE_DISCORD = bool(aws_ddns_config["USE_DISCORD"])
    DISCORD_WEB_HOOK_URI = ""
    if USE_DISCORD:
        if "DISCORD_WEB_HOOK_URI" not in aws_ddns_config:
            raise Exception("DISCORD_WEB_HOOK_URI is not in config.json")
        DISCORD_WEB_HOOK_URI = str(aws_ddns_config["DISCORD_WEB_HOOK_URI"])
            
    AWS_ACCESS_KEY_ID = str(aws_ddns_config["AWS_ACCESS_KEY_ID"])
    AWS_SECRET_ACCESS_KEY = str(aws_ddns_config["AWS_SECRET_ACCESS_KEY"])
    
    CONFIG_HOSTED_ZONES = aws_ddns_config["HostedZones"]

except Exception as e:
    print(f'Failed to get config: {e} \nPlease check the config.json')
    exit(1)
