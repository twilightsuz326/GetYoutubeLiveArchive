#
# ChannelSearch
# Author: TwilightSuz326
#
# 直近7日のライブ配信の動画IDのみ抽出する
#

# -*- coding: utf-8 -*-

import json
import datetime
from APIKEY import *

from googleapiclient.discovery import build


class ChannelSearch:
    def __init__(self, CHANNELID):
        self.APIKEY = APIKEY
        self.CHANNELID = CHANNELID
        self.movielist = []
        self.livemovielist = []

        self.youtube = build(
            "youtube", 
            "v3", 
            developerKey=self.APIKEY
        )

    def GetChannelMovie(self):
        response = self.youtube.search().list(
            part = "snippet",
            channelId = self.CHANNELID,
            maxResults = 25,
            order = "date" #日付順にソート
            ).execute()
        
        for item in response.get("items", []):
            if "none" == item["snippet"]["liveBroadcastContent"]:
                self.movielist.append(item["id"]["videoId"])

    def GetLiveArchive(self):
        response = self.youtube.videos().list(
            part = "liveStreamingDetails",
            id = self.movielist, 
            ).execute()

        for item in response.get("items", []):
            if "liveStreamingDetails" in item:
                if (datetime.datetime.strptime(item["liveStreamingDetails"]["actualStartTime"], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=9) >= datetime.datetime.now() - datetime.timedelta(days=7)):
                    self.livemovielist.append(item["id"])

    def main(self):
        self.GetChannelMovie()
        self.GetLiveArchive()

if __name__ == '__main__':
    cs = ChannelSearch("UCHog7L3CzsDg2GH9aza1bPg")
    cs.main()