from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from isodate import parse_duration
from datetime import timedelta

# создал .env файл в котором храню API_KEY
load_dotenv()


class PlayList:
    api_key = os.getenv("YOU_API_KEY")

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title: str = self.playlist_data()['items'][0]['snippet']['title'][:-13]
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    def playlist_data(self):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails, snippet',
                                                       maxResults=50,
                                                       ).execute()
        return playlist_videos

    @property
    def total_duration(self):
        """Суммарная длительность плэйлиста"""

        youtube = build('youtube', 'v3', developerKey=self.api_key)
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_data()['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        durations = []
        for item in video_response['items']:
            duration = item['contentDetails']['duration']
            parsed_duration = parse_duration(duration)
            durations.append(parsed_duration)
            total_duration = sum(durations, timedelta())

        return total_duration

    def show_best_video(self):
        """Получение id самого популярного видео по кол. просмотров"""

        youtube = build('youtube', 'v3', developerKey=self.api_key)
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_data()['items']]
        video_response = youtube.videos().list(part='statistics, contentDetails',
                                               id=','.join(video_ids)
                                               ).execute()

        max_views = 0
        best_video_id = ''

        for i in video_response['items']:
            view_count = int(i['statistics']['viewCount'])
            if view_count > max_views:
                max_views = view_count
                best_video_id = i['id']
        return 'https://youtu.be/' + best_video_id
