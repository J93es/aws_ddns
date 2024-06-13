from controller.fetch import to_discord

def logger(text: str, sender: str = "AWS DDNS") -> None:
    content: str = f'[{sender}] {text}'
    to_discord(content)