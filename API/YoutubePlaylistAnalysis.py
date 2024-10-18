""" This script defines a class `YoutubePlaylistAnalysis` that interacts with the YouTube Data API to analyze videos
    in a specified playlist. It retrieves video IDs and their associated statistics, including title, duration,
    publication date, like count, and view count. The data is organized into a pandas DataFrame, and a bar plot is
    generated using Seaborn to visualize the view counts of the videos, sorted in descending order. The bar plot is
    annotated with video IDs for easy reference.
"""


import json
import os
import isodate
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import googleapiclient.discovery
import pandas
import pandas as pd


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


if __name__ == '__main__':
    playlistInsights = YoutubePlaylistAnalysis()
    increment = 1

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
                'indices': increment,
                'video_id': items.get('id'),
                'title': items['snippet'].get('title'),
                'duration': isodate.parse_duration(duration).total_seconds(),
                'publised_date': items['snippet'].get('publishedAt'),
                'like_count': items['statistics'].get('likeCount'),
                'views_count': items['statistics'].get('viewCount')
            }])
            increment +=1

            data_frame = pandas.concat([data_frame,data], ignore_index=True)
    data_frame['publised_date'] = pandas.to_datetime(data_frame['publised_date'])
    data_frame['publised_date'] = data_frame['publised_date'].dt.strftime('%Y-%m-%d')

    numeric_cols = ['duration','like_count','views_count']
    data_frame[numeric_cols] = data_frame[numeric_cols].apply(pd.to_numeric, errors='coerce', axis=1)


    def graph_visualization():
        sorted = data_frame.sort_values('views_count', ascending=False)
        # Create the bar plot
        ax = sns.barplot(x=data_frame.index, y='views_count',data=sorted)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x/1000:.0f}k"))
        ax.set_xticks(range(len(ax.get_xticklabels())))  # Setting the ticks
        # Rotate x-axis labels for better readability
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

        # Annotate each bar with its respective title
        for i, bar in enumerate(ax.patches):
            ax.text(
                bar.get_x() + bar.get_width() / 2,  # X-coordinate (center of the bar)
                bar.get_height(),  # Y-coordinate (top of the bar)
                " " + sorted.iloc[i]['video_id'],
                # The title to be displayed
                ha='center',  # Horizontal alignment to center the text above the bar
                va='bottom',  # Vertical alignment to ensure the text is placed slightly above the bar
                rotation=90,  # Rotate the text for vertical display
                fontsize=10,  # Adjust fontsize if needed
                color='black'  # Color of the text
            )
        ax.set_xticks(range(len(sorted['indices'])))  # Setting the ticks
        ax.set_xticklabels(sorted['indices'], rotation=90)  # Setting the labels
        plt.xlabel('indices')

        # Display the plot
        plt.show()


    graph_visualization()
