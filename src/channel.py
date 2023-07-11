from dotenv import load_dotenv
import os
from googleapiclient.discovery import build

# создал .env файл в котором храню API_KEY
load_dotenv()

class Channel:
    def __init__(self, channel_id: str):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = os.getenv("YOU_API_KEY")


    def print_info(self):
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        print(channel)
