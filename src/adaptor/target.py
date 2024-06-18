from schema.hosted_zone import HostedZones
      
class TargetHostedZones(HostedZones):
    hosted_zones: list
    
    def __init__(self, config_hosted_zones: list) -> None:
        hosted_zones = self.__init_filter_hosted_zones(config_hosted_zones)
        self.hosted_zones = HostedZones(hosted_zones)
            
    def __init_filter_hosted_zones(self, config_hosted_zones: list) -> list:
        hosted_zones = []
        for config_hosted_zone in config_hosted_zones:
            config_hosted_zone['Id'] = ''
            if 'Comment' not in config_hosted_zone:
                config_hosted_zone['Comment'] = None
            config_hosted_zone['Records'] = self.__init_filter_records(config_hosted_zone['Records'])
            
            hosted_zones.append(config_hosted_zone)
        return hosted_zones
    
    def __init_filter_records(self, config_records: list) -> dict:
        records = []
        for config_record in config_records:
            config_record['Resource'] = []
            records.append(config_record)
        return records

#config.py