from controller.fetch import to_discord

def logger(text: str, sender: str = "ROUTE53 DDNS") -> None:
    content: str = f'[{sender}] {text}'
    to_discord(content)