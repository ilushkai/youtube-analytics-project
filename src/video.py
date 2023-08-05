from dotenv import load_dotenv
import os
from googleapiclient.discovery import build

# создал .env файл в котором храню API_KEY
load_dotenv()


class Video:
    api_key = os.getenv("YOU_API_KEY")

    def __init__(self, video_id):
        self.video_id = video_id
        try:
            self.title: str = self.video_data()['items'][0]['snippet']['title']
            self.url_video = 'https://www.youtube.com/watch?v=' + self.video_id
            self.view_count: int = self.video_data()['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_data()['items'][0]['statistics']['likeCount']

        except IndexError:
            self.title = None
            self.url_video = None
            self.view_count = None
            self.like_count = None


    def video_data(self):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()
        return video_response

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.id_playlist = id_playlist


broken_video = Video('broken_video_id')
