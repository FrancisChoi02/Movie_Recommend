class AoaiResponse:
    created: int
    reply: dict
    tokenCount: int

    def __init__(self, resp: dict) -> None:
        self.created = resp.get('created')
        self.reply = resp.get('choices')[0].get('message').get('content')
        self.tokenCount = resp.get('usage').get('total_tokens')