#!/usr/bin/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import timezone, datetime, timedelta

# DEVELOPER_KEY comes from a google cloud project.
DEVELOPER_KEY = 'AIzaSyCphGCNKcetS7iXLVBDCnRTVkdX01LugSg'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
END_DATE = (datetime.now(timezone.utc).astimezone()).isoformat()
START_DATE = (datetime.now(timezone.utc).astimezone() - timedelta(days=1)).isoformat()
CLIENT = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
               developerKey=DEVELOPER_KEY)


def youtube_search():
    search_response = CLIENT.search().list(
        q='landslide',
        part='id,snippet',
        order='viewCount',
        type='video',
        publishedAfter=START_DATE,
        publishedBefore=END_DATE,
        maxResults=10
    ).execute()

    videos = []

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('{}\t{}\t{}'.format(search_result['id']['videoId'],
                                              search_result['snippet']['title'],
                                              get_viewCount(search_result['id']['videoId'])))

    print('{}\t{}\n'.format(START_DATE, END_DATE))
    print('\n'.join(videos))


def get_viewCount(vid_id):
    response = CLIENT.videos().list(
        part='statistics',
        id=vid_id
    ).execute()
    return response['items'][0]['statistics']['viewCount']


if __name__ == '__main__':
    try:
        youtube_search()
    except HttpError as e:
        print('An HTTP error {} occurred:\n{}'.format(e.resp.status, e.content))
