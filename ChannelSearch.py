#
# ChannelSearch
# Author: TwilightSuz326
#
# 直近7日のライブ配信の動画IDのみ抽出する
#

# -*- coding: utf-8 -*-

import os
import json
import datetime
from GetYoutubeLiveArchive.APIKEY import *

from googleapiclient.discovery import build
from googleapiclient.errors import *


class ChannelSearch:
    def __init__(self, CHANNELID, key=0):
        self.key = readkey()
        self.APIKEY = APIKEY[0]
        self.CHANNELID = CHANNELID
        self.movielist = []
        self.livemovielist = []
        self.rebuild()
        #self.youtube = self.rebuild()

    def rebuild(self):
        self.APIKEY = APIKEY[self.key]
        self.youtube = build(
            "youtube", 
            "v3", 
            developerKey=self.APIKEY
        )

    def GetChannelMovie(self):
        response = self.youtube.search().list(
            part = "snippet",
            channelId = self.CHANNELID,
            maxResults = 7,
            order = "date" #日付順にソート
        ).execute()
        
        for item in response.get("items", []):
            if "none" == item["snippet"]["liveBroadcastContent"]:
                if "videoId" in item["id"]:
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
        try:
            self.GetChannelMovie()
            self.GetLiveArchive()
        except HttpError as g:
            print("★API KEY ERROR!★ => {}".format(self.key +1))
            if len(self.APIKEY) -1 > self.key:
                self.key += 1
                writekey(self.key)
                self.rebuild()
                self.main()
                return
            else:
                print("APIKEYないからおわり")
                raise Exception('NO APIKEY', 'eggs')

def readkey():
    if(os.path.isfile('key.txt')):
        with open('key.txt') as f:
            k = f.read()
        return int(k)
    else:
        writekey(0)
        return 0

def writekey(key):
    with open('key.txt','w', newline='', encoding="utf_8") as f:
        f.write(str(key))

if __name__ == '__main__':
    cs = ChannelSearch("UCHog7L3CzsDg2GH9aza1bPg")
    cs.main()
    print(cs.movielist)