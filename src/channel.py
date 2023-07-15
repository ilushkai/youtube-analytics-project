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
        self.title = self.info()['items'][0]['snippet']['title']
        self.description = self.info()['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count = self.info()['items'][0]['statistics']['subscriberCount']
        self.video_count = self.info()['items'][0]['statistics']['videoCount']
        self.view_count = self.info()['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    def info(self):
        """Возвращает в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        return channel

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        return print(channel)

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
