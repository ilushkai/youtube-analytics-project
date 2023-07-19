from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import json

# создал .env файл в котором храню API_KEY
load_dotenv()


class Channel:
    api_key = os.getenv("YOU_API_KEY")

    def __init__(self, channel_id: str):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        # self.api_key = os.getenv("YOU_API_KEY")
        self.title = self.channel_date()['items'][0]['snippet']['title']
        self.description = self.channel_date()['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count = int(self.channel_date()['items'][0]['statistics']['subscriberCount'])
        self.video_count = self.channel_date()['items'][0]['statistics']['videoCount']
        self.view_count = self.channel_date()['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __rsub__(self, other):
        return other.subscriber_count - self.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    @property
    def channel_id(self):
        return self.__channel_id

    def channel_date(self):
        """Возвращает в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        return channel

    @classmethod
    def get_service(cls):
        """получение обекта youtube API"""
        service = build('youtube', 'v3', developerKey=cls.api_key)

        return service

    def to_json(self, filedate):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`"""
        data = {
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(filedate, "w") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
