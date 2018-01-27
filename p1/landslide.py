#!/usr/bin/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import rfc3339
import os

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
END_DATE = datetime.now()
START_DATE = datetime.now() - timedelta(days=1)


def youtube_search(client):
    search_response = client.search().list(
        q='landslide',
        part='id,snippet',
        order='viewCount',
        type='video',
        publishedAfter=rfc3339.rfc3339(START_DATE),
        publishedBefore=rfc3339.rfc3339(END_DATE),
        maxResults=10
    ).execute()

    videos = []

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('{}\t{}\t{}'.format(search_result['id']['videoId'],
                                              search_result['snippet']['title'].encode('utf-8'),
                                              get_viewCount(client, search_result['id']['videoId'])))

    print '{}\t{}\n'.format(START_DATE, END_DATE)
    print '\n'.join(videos)


def get_viewCount(client, vid_id):
    response = client.videos().list(
        part='statistics',
        id=vid_id
    ).execute()
    return response['items'][0]['statistics']['viewCount']


if __name__ == '__main__':
    try:
        client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                       developerKey=os.environ['YT_DEV_KEY'])
        youtube_search(client)
    except KeyError:
        print 'Please set your YT_DEV_KEY environment variable.'
    except HttpError, e:
        print('An HTTP error {} occurred:\n{}'.format(e.resp.status, e.content))
