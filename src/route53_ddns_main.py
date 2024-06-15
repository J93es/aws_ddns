from route53_ddns_config import CONFIG_HOSTED_ZONES
from adapter.route53 import Route53_Hosted_Zones
from adapter.target import Target_Hosted_Zones
from service.logger import logger
from service.updater import Updater
from controller.fetch import get_current_ip

def route53_ddns():
    try: 
        current_ip = get_current_ip()
    except Exception as e:
        logger(f'Failed to get current ip: {e}')
        exit(1)
        
        
    try:
        target_hosted_zones = Target_Hosted_Zones(CONFIG_HOSTED_ZONES)
    except Exception as e:
        logger(f'Failed to get config: {e} \nPlease check the config.json')
        exit(1)


    try:  
        route53_hosted_zones = Route53_Hosted_Zones(target_hosted_zones)
    except Exception as e:
        logger(f'Failed to get hosted zones: {e}')
        exit(1)
        
        
    try:
        updater = Updater(route53_hosted_zones, target_hosted_zones, current_ip)
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


route53_ddns()