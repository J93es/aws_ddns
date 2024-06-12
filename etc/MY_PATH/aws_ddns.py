import boto3
import urllib.request
import urllib.parse
# import requests

from config import aws_ddns_config

try:
    USE_DISCORD = bool(aws_ddns_config["USE_DISCORD"])
    DISCORD_WEB_HOOK_URI = ""
    if USE_DISCORD:
        DISCORD_WEB_HOOK_URI = str(aws_ddns_config["DISCORD_WEB_HOOK_URI"])
        
    AWS_ACCESS_KEY_ID = str(aws_ddns_config["AWS_ACCESS_KEY_ID"])
    AWS_SECRET_ACCESS_KEY = str(aws_ddns_config["AWS_SECRET_ACCESS_KEY"])

    conf_hosted_zones = aws_ddns_config["hostedZones"]
    
    for conf_hosted_zone_name in conf_hosted_zones:
        if "Comment" in conf_hosted_zones[conf_hosted_zone_name]:
            conf_hosted_zones[conf_hosted_zone_name]["Comment"] = str(conf_hosted_zones[conf_hosted_zone_name]["Comment"]).strip()
            
        conf_records = conf_hosted_zones[conf_hosted_zone_name]["records"]
        for conf_record_name in conf_records:
            if "TTL" in conf_records[conf_record_name]:
                conf_records[conf_record_name]["TTL"] = \
                    int(conf_records[conf_record_name]["TTL"])
            else:
                conf_records[conf_record_name]["TTL"] = 300
except Exception as e:
    print(f'Failed to get config: {e}')
    print('Please check the config file.')
    exit(1)



def to_discord(content: str) -> None:
    try:
        if not USE_DISCORD or DISCORD_WEB_HOOK_URI == "":
            return
        
        data = { 'content': f'\n\n{content}' }
        data = urllib.parse.urlencode(data).encode('utf-8')
        request = urllib.request.Request(DISCORD_WEB_HOOK_URI, data=data)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        with urllib.request.urlopen(request) as response:
            if response.status != 204:
                print(f'Failed to send message to Discord: {response.status}')
        
        # # *** If use requests module instead of urllib.request ***
        # res = requests.post(url=DISCORD_WEB_HOOK_URI, json={ "content": content }, headers={"Content-Type": "application/json"})
        # if res.status_code != 204:
        #     print(f'Failed to send message to Discord: {res.text}')
    except Exception as e:
        print(f'Failed to send message to Discord | {e}')


def logging(text: str, sender: str = "AWS DDNS") -> None:
    content: str = f'[{sender}] {text}'
    to_discord(content)


def get_cur_ip() -> str:
    
    with urllib.request.urlopen("https://checkip.amazonaws.com") as response:
        if response.status != 200:
            raise Exception(f'response status: {response.status}')
        cur_ip: str = response.read().decode("utf-8").strip()
        
    # # *** If use requests module instead of urllib.request ***
    # response = requests.get("https://checkip.amazonaws.com")
    # if response.status_code != 200:
    #     raise Exception(f'response status: {response.status_code}')
    # cur_ip: str = response.text.strip()
    return cur_ip


def get_client() -> boto3.client:
    client: boto3.client = boto3.client('route53', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    return client


def get_hosted_zones_list(client: boto3.client) -> list:
    response = client.list_hosted_zones()
    return response['HostedZones']


def filter_hosted_zones(hosted_zones: list, conf_hosted_zones: dict) -> list:
    filtered_hosted_zones: list = []
    for each_hosted_zone in hosted_zones:
        each_hosted_zone['Name'] = each_hosted_zone['Name'][:-1]
        hosted_zone_name: str = each_hosted_zone['Name']
        
        if hosted_zone_name not in conf_hosted_zones:
            continue
        
        if "Comment" not in conf_hosted_zones[hosted_zone_name]:
            filtered_hosted_zones.append(each_hosted_zone)
            continue
        
        if each_hosted_zone["Config"]["Comment"].strip() == conf_hosted_zones[hosted_zone_name]["Comment"]:
            filtered_hosted_zones.append(each_hosted_zone)
            continue
        
    return filtered_hosted_zones
    

def upsert_records(client: boto3.client, hosted_zone_id: str, change_batch: list) -> None:    
    response = client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': change_batch
        }
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise Exception(f'HTTPStatusCode is not 200: {response}')
    


def get_records(client: boto3.client, hosted_zone_id: str) -> list:
    response = client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id
    )
    return response['ResourceRecordSets']


def filter_records(records: list, conf_records: dict) -> list:
    filtered_records: list = []
    for each_record in records:
        each_record['Name'] = each_record['Name'][:-1]
        if each_record['Type'] != 'A':
            continue
        if each_record['Name'] in conf_records:
            filtered_records.append(each_record)
            continue
    return filtered_records


def make_change_batch(records: list, conf_records: dict, cur_ip: str) -> list:
    change_batch: list = []
    
    def is_ip_maintained(record: dict, cur_ip: str) -> bool:
        for each_record in record['ResourceRecords']:
            if each_record['Value'] == cur_ip:
                return True
        return False
    
    for each_record in records:
        record_name: str = each_record['Name']
        ttl_vaule: str = conf_records[record_name]['TTL']
            
        if is_ip_maintained(record=each_record, cur_ip=cur_ip) and int(each_record['TTL']) == int(ttl_vaule):
            continue
        
        change_batch.append({
            'Action': u'UPSERT',
            'ResourceRecordSet': {
                'Name': record_name,
                'Type': 'A',
                'TTL': ttl_vaule,
                'ResourceRecords': [
                    {
                        'Value': cur_ip
                    }
                ]
            }
        })
    
    return change_batch


def make_upsert_success_log(hosted_zone_name: str, change_batch: list) -> str:
    success_log = ''
    success_log += "Success to update\n"
    success_log += f'--------hosted zone: {hosted_zone_name}--------\n'
    
    for each_change in change_batch:
        change_record = each_change['ResourceRecordSet']
        head = f'\t----record set: {change_record["Name"]}----\n'
        body = f'\t\tTTL: {change_record["TTL"]}\n'
        body += f'\t\tip: {change_record["ResourceRecords"]}\n'
        tail = f'\t{"-" * (len(head) - 2)}\n'
        
        success_log += head + body + tail
        
    success_log += "---------------------\n"
    
    return success_log



# main
try:
    cur_ip: str = get_cur_ip()   
except Exception as e:
    logging(f'Failed to get current IP address from "https://checkip.amazonaws.com" \nerror: {e}', "get_cur_ip()")
    exit(1)
   
try:
    client: boto3.client = get_client()
except Exception as e:
    logging(f'Failed to get aws client \nerror: {e}', "get_aws_client()")
    exit(1)
    
try:
    hosted_zones: list = get_hosted_zones_list(client)
except Exception as e:
    logging(f'Failed to get hosted zones \nerror: {e}', "get_hosted_zones_list()")
    exit(1)

hosted_zones: list = filter_hosted_zones(hosted_zones=hosted_zones, conf_hosted_zones=conf_hosted_zones)

for each_hosted_zone in hosted_zones:
    try:
        hosted_zone_id: str = each_hosted_zone["Id"]
        hosted_zone_name: str = each_hosted_zone['Name']
        
        try:
            records: list = get_records(client=client, hosted_zone_id=hosted_zone_id)
        except Exception as e:
            logging(f'Failed to get resource record sets from hosted zone: {hosted_zone_name} \nerror: {e}', "get_records()")
            continue

        conf_records: dict = conf_hosted_zones[hosted_zone_name]['records']
        records = filter_records(records=records, conf_records=conf_records)
        change_batch = make_change_batch(records=records, conf_records=conf_records, cur_ip=cur_ip)
        
        if len(change_batch) == 0:
            continue

        try:
            upsert_records(client=client, hosted_zone_id=hosted_zone_id, change_batch=change_batch)
            success_log = make_upsert_success_log(hosted_zone_name, change_batch)
            logging(f'{success_log}')
        except Exception as e:
            logging(f'Failed to update hosted zone: {hosted_zone_name}', "upsert_records()")
            continue
                
    except Exception as e:
        logging(f'failed to update: {hosted_zone_name} \nerror: {e}')
        continue
    