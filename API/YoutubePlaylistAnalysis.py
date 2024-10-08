import json
import os
import isodate

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

    def get_video_statistics(self, videolist=None) -> []:
        data = []
        if videolist is None:
            raise ValueError('No videos found...')
        batch_size = 50
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
            for items in response['items']:
                duration = items['contentDetails'].get('duration')
                data.append([{
                    'video_id': items.get('id'),
                    'title': items['snippet'].get('title'),
                    'tags': items['snippet'].get('tags'),
                    'duration': isodate.parse_duration(duration).total_seconds(),
                    'publised_date': items['snippet'].get('publishedAt'),
                    'like_count': items['statistics'].get('likeCount'),
                    'views_count': items['statistics'].get('viewCount')
                }])
        return data


if __name__ == '__main__':
    playlistInsights = YoutubePlaylistAnalysis()

    playlistid = 'PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH'
    video_ids = playlistInsights.get_video_ids(playlistid)

    # dataframe = pandas.DataFrame(playlistInsights.get_video_statistics(video_ids))
    data_frame = pandas.DataFrame()
    batch_size = 50
    for i in range(0, len(video_ids), batch_size):
        j = i + batch_size
        if j >= len(video_ids):
            j = len(video_ids) - 1
        videoIds = ','.join(video_ids[i:j])
        request = playlistInsights.get_request().videos().list(
            part='snippet, contentDetails, statistics',
            id=videoIds
        )
        response = request.execute()
        for items in response['items']:
            duration = items['contentDetails'].get('duration')
            data = pandas.DataFrame([{
                'video_id': items.get('id'),
                'title': items['snippet'].get('title'),
                'tags': items['snippet'].get('tags'),
                'duration': isodate.parse_duration(duration).total_seconds(),
                'publised_date': items['snippet'].get('publishedAt'),
                'like_count': items['statistics'].get('likeCount'),
                'views_count': items['statistics'].get('viewCount')
            }])

            data_frame = pandas.concat([data_frame,data], ignore_index=True)
    print(data_frame)
    data_frame = data_frame.drop('tags',axis=1)
    data_frame.to_excel('C:/Users/deval/OneDrive/Desktop/Programing/data handling/Data Gathering '
                        'Projects/videoInformation.xlsx')