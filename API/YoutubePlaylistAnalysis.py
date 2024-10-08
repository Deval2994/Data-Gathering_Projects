import json
import os
import isodate
import matplotlib.pyplot as plt
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
                'duration': isodate.parse_duration(duration).total_seconds(),
                'publised_date': items['snippet'].get('publishedAt'),
                'like_count': items['statistics'].get('likeCount'),
                'views_count': items['statistics'].get('viewCount')
            }])

            data_frame = pandas.concat([data_frame,data], ignore_index=True)
    data_frame['publised_date'] = pandas.to_datetime(data_frame['publised_date'])
    data_frame['publised_date'] = data_frame['publised_date'].dt.strftime('%Y-%m-%d')

    numeric_cols = ['duration','like_count','views_count']
    data_frame[numeric_cols] = data_frame[numeric_cols].apply(pd.to_numeric, errors='coerce', axis=1)

    data_frame['indexing'] = data_frame.index + 1
    cols = data_frame.columns.tolist()
    new_order = [cols[-1]] + cols[:-1]
    data_frame = data_frame[new_order]

    def graph_visualization():
        # Sort data frame by views count and take the top 10
        df = data_frame.sort_values('views_count', ascending=False)

        # Create the bar plot
        ax = sns.barplot(x=data_frame['indexing'], y='views_count', data=df)

        # Add titles above the bars
        for i, bar in enumerate(ax.patches):
            ax.text(
                bar.get_x() + bar.get_width() / 2,  # X-coordinate (center of the bar)
                bar.get_height(),  # Y-coordinate (top of the bar)
                "  "+df.iloc[i]['video_id'],  # The title to be displayed
                ha='center',  # Horizontal alignment to center the text above the bar
                va='bottom',  # Vertical alignment to ensure the text is placed slightly above the bar
                fontsize=10,  # Adjust fontsize if needed
                rotation=90,
                color='black'  # Color of the text
            )

        # Show the plot
        plt.show()


    graph_visualization()
