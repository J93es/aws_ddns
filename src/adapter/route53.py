from schema.hosted_zone import Hosted_Zones, Each_Hosted_Zone_Distinction
from schema.record import Records, Each_Record_Distinction
from controller.boto3_controller import boto3_controller

class Route53_Hosted_Zones(Hosted_Zones):
    hosted_zones: list
    
    
    def __init__(self, target_hosted_zone: Hosted_Zones) -> None:
        route53_hosted_zones = self.__init_hosted_zones(target_hosted_zone)
        self.hosted_zones = Hosted_Zones(route53_hosted_zones)
            
            
    def __init_hosted_zones(self, target_hosted_zone: Hosted_Zones) -> list:
        hosted_zones = []
        route53_hosted_zones = boto3_controller.get_hosted_zones()
        target_hosted_zone_distinctions = target_hosted_zone.get_distinctions()

        for route53_hosted_zone in route53_hosted_zones:
            route53_hosted_zone['Name'] = route53_hosted_zone['Name'][:-1]
            route53_hosted_zone['Comment'] = route53_hosted_zone['Config'].pop('Comment')
            
            route53_hosted_zone_distinction = Each_Hosted_Zone_Distinction(route53_hosted_zone['Name'], route53_hosted_zone['Comment'])
            if target_hosted_zone_distinctions != None and route53_hosted_zone_distinction not in target_hosted_zone_distinctions:
                continue
            
            target_records: Records = target_hosted_zone.find_by_distinction(route53_hosted_zone_distinction).get_records()
            route53_hosted_zone['Records'] = self.__init_records(route53_hosted_zone['Id'], target_records)
            
            hosted_zones.append(route53_hosted_zone)
        return hosted_zones
    
    
    def __init_records(self, hosted_zone_id: str, target_records: Records) -> list:
        records = []
        route53_records = boto3_controller.get_records(hosted_zone_id)
        target_records_distinctions = target_records.get_distinctions()
        
        for route53_record in route53_records:
            route53_record['Name'] = route53_record['Name'][:-1]
            if route53_record['Type'] != 'A':
                continue
            
            route53_record_distinction = Each_Record_Distinction(route53_record['Name'])
            if route53_record_distinction not in target_records_distinctions:
                continue
            
            route53_record['Resource'] = route53_record.pop('ResourceRecords')
            records.append(route53_record)
        return records



# from config import route53_ddns_config
# from repository.target import Target_Hosted_Zones

# print(route53_ddns_config["HostedZones"])
# target_hosted_zones = Target_Hosted_Zones(route53_ddns_config["HostedZones"])

# route53_ACCESS_KEY_ID = str(route53_ddns_config["route53_ACCESS_KEY_ID"])
# route53_SECRET_ACCESS_KEY = str(route53_ddns_config["route53_SECRET_ACCESS_KEY"])

# route53_hosted_zones = route53_Hosted_Zones(target_hosted_zones)
# print(target_hosted_zones.to_list())
# print(route53_hosted_zones.to_list())
        
# https://boto3.amazonroute53.com/v1/documentation/api/latest/reference/services/route53/client/list_resource_record_sets.html    
# list_resource_record_sets__response
# {
#     'ResourceRecordSets': [
#         {
#             'Name': 'string',
#             'Type': 'SOA'|'A'|'TXT'|'NS'|'CNAME'|'MX'|'NAPTR'|'PTR'|'SRV'|'SPF'|'AAAA'|'CAA'|'DS',
#             'SetIdentifier': 'string',
#             'Weight': 123,
#             'Region': 'us-east-1'|'us-east-2'|'us-west-1'|'us-west-2'|'ca-central-1'|'eu-west-1'|'eu-west-2'|'eu-west-3'|'eu-central-1'|'eu-central-2'|'ap-southeast-1'|'ap-southeast-2'|'ap-southeast-3'|'ap-northeast-1'|'ap-northeast-2'|'ap-northeast-3'|'eu-north-1'|'sa-east-1'|'cn-north-1'|'cn-northwest-1'|'ap-east-1'|'me-south-1'|'me-central-1'|'ap-south-1'|'ap-south-2'|'af-south-1'|'eu-south-1'|'eu-south-2'|'ap-southeast-4'|'il-central-1'|'ca-west-1',
#             'GeoLocation': {
#                 'ContinentCode': 'string',
#                 'CountryCode': 'string',
#                 'SubdivisionCode': 'string'
#             },
#             'Failover': 'PRIMARY'|'SECONDARY',
#             'MultiValueAnswer': True|False,
#             'TTL': 123,
#             'ResourceRecords': [
#                 {
#                     'Value': 'string'
#                 },
#             ],
#             'AliasTarget': {
#                 'HostedZoneId': 'string',
#                 'DNSName': 'string',
#                 'EvaluateTargetHealth': True|False
#             },
#             'HealthCheckId': 'string',
#             'TrafficPolicyInstanceId': 'string',
#             'CidrRoutingConfig': {
#                 'CollectionId': 'string',
#                 'LocationName': 'string'
#             },
#             'GeoProximityLocation': {
#                 'route53Region': 'string',
#                 'LocalZoneGroup': 'string',
#                 'Coordinates': {
#                     'Latitude': 'string',
#                     'Longitude': 'string'
#                 },
#                 'Bias': 123
#             }
#         },
#     ],
#     'IsTruncated': True|False,
#     'NextRecordName': 'string',
#     'NextRecordType': 'SOA'|'A'|'TXT'|'NS'|'CNAME'|'MX'|'NAPTR'|'PTR'|'SRV'|'SPF'|'AAAA'|'CAA'|'DS',
#     'NextRecordIdentifier': 'string',
#     'MaxItems': 'string'
# }