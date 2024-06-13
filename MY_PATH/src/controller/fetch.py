import urllib.request
import urllib.parse
from aws_ddns_main import aws_ddns_config


USE_DISCORD = bool(aws_ddns_config["USE_DISCORD"])
DISCORD_WEB_HOOK_URI = ""
if USE_DISCORD:
    DISCORD_WEB_HOOK_URI = str(aws_ddns_config["DISCORD_WEB_HOOK_URI"])
    
    
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
        
        
def get_current_ip() -> str:
    
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
      