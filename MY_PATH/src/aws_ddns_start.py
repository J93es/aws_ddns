from aws_ddns_main import aws_ddns_config
from adapter.aws import AWS_Hosted_Zones
from adapter.target import Target_Hosted_Zones
from service.logger import logger
from service.updater import Updater
from controller.fetch import get_current_ip

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
        DISCORD_WEB_HOOK_URI = str(aws_ddns_config["DISCORD_WEB_HOOK_URI"])
            
    AWS_ACCESS_KEY_ID = str(aws_ddns_config["AWS_ACCESS_KEY_ID"])
    AWS_SECRET_ACCESS_KEY = str(aws_ddns_config["AWS_SECRET_ACCESS_KEY"])
    
    target_hosted_zones = Target_Hosted_Zones(aws_ddns_config["HostedZones"])

except Exception as e:
    logger(f'Failed to get config: {e} \nPlease check the config.json')
    exit(1)
        

def aws_ddns():
    try: 
        current_ip = get_current_ip()
    except Exception as e:
        logger(f'Failed to get current ip: {e}')
        exit(1)


    try:  
        aws_hosted_zones = AWS_Hosted_Zones(target_hosted_zones)
    except Exception as e:
        logger(f'Failed to get hosted zones: {e}')
        exit(1)
        
    try:
        updater = Updater(aws_hosted_zones, target_hosted_zones, current_ip)
        updater.update_hosted_zone()
    except Exception as e:
        logger(f'Failed to update hosted zones: {e}')
        exit(1)
        
    try:
        log = updater.make_log()
        if len(log) != 0:
            logger(log)
    except Exception as e:
        logger(f'Failed to send log: {e}')
        exit(1)

aws_ddns()