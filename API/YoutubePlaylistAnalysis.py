import json

import googleapiclient.discovery
import pandas


class YoutubePlaylistAnalysis:
    def __init__(self):
        self.service_name = 'youtube'
        self.api_version = 'v3'
        self.API_KEY = 'AIzaSyABP4i5X9s8euy75WEJdl05_6woUDqH4hk'

    def get_request(self):
        return googleapiclient.discovery.build(serviceName=self.service_name, version=self.api_version,
                                               developerKey=self.API_KEY)

    def get_video_ids(self, playlist=None):
        if playlist is None:
            raise ValueError('No Playlist found')
        videoIds = []
        request = self.get_request().playlistItems().list(
            part='snippet, contentDetails',
            playlistId=playlist,
            maxResults=50
        )
        response = request.execute()
        for items in response['items']:
            videoIds.append(items['contentDetails']['videoId'])

        nextPage = response.get('nextPageToken')
        while nextPage is not None:
            request = self.get_request().playlistItems().list(
                part='snippet, contentDetails',
                playlistId=playlist,
                maxResults=50,
                pageToken=nextPage
            )
            response = request.execute()
            for items in response['items']:
                videoIds.append(items['contentDetails']['videoId'])
            nextPage = response.get('nextPageToken')

        return videoIds

    def get_video_statistics(self, videolist=None):
        if videolist is None:
            raise ValueError('No videos found...')
        batch_size = 50
        print(len(videolist))
        for i in range(0, len(videolist), batch_size):
            j = i + batch_size
            if j >= len(videolist):
                j = len(videolist) - 1
            videoIds = ','.join(videolist[i:j])
            request = self.get_request().videos().list(
                part='snippet, contentDetails, statistics',
                id=videoIds
            )
            response = request.execute()


if __name__ == '__main__':
    playlistInsights = YoutubePlaylistAnalysis()

    playlistid = 'PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH'
    video_ids = playlistInsights.get_video_ids(playlistid)
    playlistInsights.get_video_statistics(video_ids)
