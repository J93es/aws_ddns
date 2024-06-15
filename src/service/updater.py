import copy
from controller.boto3_controller import boto3_controller

class Updater:
    current_ip: str
    changed_info: list
    route53_hosted_zones: dict
    target_hosted_zones: dict
    
    def __init__(self, route53_hosted_zones: dict, target_hosted_zones: dict, current_ip: str) -> None:
        self.changed_info = []
        self.route53_hosted_zones = route53_hosted_zones
        self.target_hosted_zones = target_hosted_zones
        self.current_ip = current_ip
        
    def get_changed_info(self) -> list:
        return copy.deepcopy(self.changed_info)
      
    def make_change_batch(self, route53_records: dict, target_records: dict) -> dict:
        change_batch = []
        changed_records = []
            
        for route53_record in route53_records:
            record_distinction = route53_record.get_distinction()
            target_record = target_records.find_by_distinction(record_distinction)
            
            previous_ip_list = []
            route53_resource = route53_record.resource
            for elem in route53_resource:
                previous_ip_list.append(elem['Value']) 
            previous_ttl = route53_record.ttl
            
            current_ttl = target_record.ttl
                
            if self.current_ip in previous_ip_list and previous_ttl == current_ttl:
                continue
            
            changed_records.append({"Name" : target_record.name, "IP" : { "Previous": previous_ip_list, "Current": self.current_ip }, "TTL" : { "Previous": previous_ttl, "Current": current_ttl }})
            change_batch.append({
                'Action': u'UPSERT',
                'ResourceRecordSet': {
                    'Name': target_record.name,
                    'Type': 'A',
                    'TTL': target_record.ttl,
                    'ResourceRecords': [
                        {
                            'Value': self.current_ip
                        }
                    ]
                }
            })
            
        return change_batch, changed_records
    

    def update_hosted_zone(self) -> list:
        changed_info = []
        for route53_hosted_zone in self.route53_hosted_zones:
            hosted_zone_distinction = route53_hosted_zone.get_distinction()
            target_hosted_zone = self.target_hosted_zones.find_by_distinction(hosted_zone_distinction)
            
            route53_records = route53_hosted_zone.get_records()
            target_records = target_hosted_zone.get_records()
            change_batch, changed_records = self.make_change_batch(route53_records, target_records)  
                    
            try:
                if len(change_batch) == 0:
                    continue
                boto3_controller.upsert_records(route53_hosted_zone.id, change_batch)
                changed_info.append({"Name": route53_hosted_zone.name, "Status" : "SUCCESS","Records": changed_records})
            except Exception as e:
                changed_info.append({"Name": route53_hosted_zone.name, "Status": "Failed", "Records": f'[{changed_records}] {e}'})
                continue
                
                
        self.changed_info = changed_info
        
        
    def make_success_log(self, each_info) -> str:
        success_log = "Success to update\n"
        
        hosted_zone_head = f'--------hosted zone: {each_info["Name"]}--------\n'
        
        hosted_zone_body = ''
        for each_record in each_info["Records"]:
            record_head = f'\t----record set: {each_record["Name"]}----\n'
            record_body = f'\t\tTTL: {each_record["TTL"]["Previous"]} to {each_record["TTL"]["Current"]}\n'
            record_body += f'\t\tip: {each_record["IP"]["Previous"]} to {each_record["IP"]["Current"]}\n'
            record_tail = f'\t{"-" * (len(record_head) - 2)}\n'
            
            hosted_zone_body += record_head + record_body + record_tail
            
        hosted_zone_tail = f'{"-" * len(hosted_zone_head)}\n\n\n'
            
        return success_log + hosted_zone_head + hosted_zone_body + hosted_zone_tail

    def make_failed_log(self, each_info) -> str:
        failed_log = "Failed to update\n"
        head = f'--------hosted zone: {each_info["Name"]}--------\n'
        body = f'\t{each_info["Records"]}\n'
        tail = f'{"-" * len(head)}\n\n\n'
        
        return failed_log + head + body + tail
            
    
    def make_log(self) -> str:
        success_log = ''
        failed_log = ''
        
        for each_info in self.changed_info:
            if each_info["Status"] == "SUCCESS":
                success_log += self.make_success_log(each_info)
            else:
                failed_log += self.make_failed_log(each_info)
        return success_log + failed_log
