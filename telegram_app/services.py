import requests

from posting_app.database import Posting


class TelegramService:
    def __init__(
            self,
            bot_token: str,
            chat_room: str
    ):
        self._bot_token = bot_token
        self._chat_room = chat_room

    def format_posting_to_message(self, posting: Posting) -> str:
        '''Formats the object into a Telegram message.'''
        msg = f'<a href="{posting.url}"><b>{posting.location}</b> </a>\n<i>{posting.price}</i>\n<i>{posting.antiquity}</i>'

        return msg

    def send_telegram_message(self, msg_text: str) -> bool:
        res = requests.post(
            f"https://api.telegram.org/bot{self._bot_token}/sendMessage",
            data={
                "chat_id": self._chat_room,
                "text": msg_text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            }
        )
        return res.ok
