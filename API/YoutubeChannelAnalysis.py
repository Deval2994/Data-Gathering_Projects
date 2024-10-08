import googleapiclient.discovery
import pandas


class YoutubeChannelAnalysis:

    def __init__(self):
        self.service_name = 'youtube'
        self.api_version = 'v3'
        self.API_KEY = 'AIzaSyABP4i5X9s8euy75WEJdl05_6woUDqH4hk'

    def get_request(self):
        return googleapiclient.discovery.build(serviceName=self.service_name, version=self.api_version,
                                               developerKey=self.API_KEY)

    def get_channel_details(self, channel_information) -> []:
        item = channel_information['items'][0]
        return [{
            'channelName': item['snippet']['title'],
            'subscribers': item['statistics']['subscriberCount'],
            'totalViews': item['statistics']['viewCount'],
            'totalVideos': item['statistics']['videoCount'],
            'countryCode': item['snippet'].get('country')
        }]


if __name__ == '__main__':
    channelInsights = YoutubeChannelAnalysis()
    channels = ['tseries', 'WWE', 'setindia', 'zeemusiccompany', 'TaylorSwift']
    youtube = channelInsights.get_request()
    data_frame = pandas.DataFrame()
    for channel in channels:
        requests = youtube.channels().list(
            part='snippet, contentDetails, statistics',
            forUsername=channel
        )
        response = requests.execute()
        current_data_frame = pandas.DataFrame(channelInsights.get_channel_details(response))
        data_frame = pandas.concat([data_frame, current_data_frame], ignore_index=True)

    print(data_frame)
