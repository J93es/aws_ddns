import os, json

try:
    config_path = os.path.dirname(os.path.abspath(__file__)) + r"/../config.json"
    with open(config_path) as fs:
        route53_ddns_config = json.load(fs)
except Exception as e:
    print(f'Failed to open config.json: {e}')
    exit(1)

try:
    if "USE_DISCORD" not in route53_ddns_config:
        raise Exception("USE_DISCORD is not in config.json")
    if "ROUTE53_DDNS_ACCESS_KEY_ID" not in route53_ddns_config:
        raise Exception("ROUTE53_DDNS_ACCESS_KEY_ID is not in config.json")
    if "ROUTE53_DDNS_SECRET_ACCESS_KEY" not in route53_ddns_config:
        raise Exception("ROUTE53_DDNS_SECRET_ACCESS_KEY is not in config.json")
    if "HostedZones" not in route53_ddns_config:
        raise Exception("HostedZones is not in config.json")

    USE_DISCORD = bool(route53_ddns_config["USE_DISCORD"])
    DISCORD_WEB_HOOK_URI = ""
    if USE_DISCORD:
        if "DISCORD_WEB_HOOK_URI" not in route53_ddns_config:
            raise Exception("DISCORD_WEB_HOOK_URI is not in config.json")
        DISCORD_WEB_HOOK_URI = str(route53_ddns_config["DISCORD_WEB_HOOK_URI"])
            
    ROUTE53_DDNS_ACCESS_KEY_ID = str(route53_ddns_config["ROUTE53_DDNS_ACCESS_KEY_ID"])
    ROUTE53_DDNS_SECRET_ACCESS_KEY = str(route53_ddns_config["ROUTE53_DDNS_SECRET_ACCESS_KEY"])
    
    CONFIG_HOSTED_ZONES = route53_ddns_config["HostedZones"]

except Exception as e:
    print(f'Failed to get config: {e} \nPlease check the config.json')
    exit(1)
