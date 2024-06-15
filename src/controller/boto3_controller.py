import boto3
from aws_ddns_config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

class Boto3Controller:
    client: boto3.client
    
    def __init__(self):
        try:
            self.client = boto3.client = boto3.client('route53', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        except Exception as e:
            raise Exception(f'[boto3.client] Failed to create client: {e}')
        
    def get_client(self) -> boto3.client:
        return self.client
    
    def upsert_records(self, hosted_zone_id: str, change_batch: list) -> None:    
        response = self.client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                'Changes': change_batch
            }
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception(f'[change_resource_record_sets] HTTPStatusCode is not 200: {response}')
        
        
    def get_hosted_zones(self) -> list:
        response = self.client.list_hosted_zones()
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception(f'[list_hosted_zones] HTTPStatusCode is not 200: {response}')
        return response['HostedZones']
    
    
    def get_records(self, hosted_zone_id: str) -> list:
        response = self.client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception(f'[list_resource_record_sets] HTTPStatusCode is not 200: {response}')
        return response['ResourceRecordSets']

    
    
boto3_controller = Boto3Controller()