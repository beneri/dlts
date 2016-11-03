#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wget
import csv
import math
import string
import os, sys, fileinput
import re
import argparse
import urllib2


## ARGS ##
parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("-f", "--format", help="144, 240, 360, 480, 720, 1080")
args = parser.parse_args()

targetUrl = args.url

videoFormat = 0
if args.format :
    videoFormat = args.format

## Init ##
lastSlash       = targetUrl.rfind('/')
baseUrl = targetUrl[0:lastSlash+1]


## STEP 1 - Get playlists ##
targetUrl = args.url

data = urllib2.urlopen(targetUrl)
chunklists = []
while 1:
    infoline = data.readline()
    chunklist = data.readline()

    # Get the resolution for the playlist
    m = re.search('RESOLUTION=(\d*)x(\d*)', infoline)
    if m:
        chunklists.append(
            (chunklist[:-1], ( int(m.group(1)), int(m.group(2)) ))
        )

    if not chunklist:
        break

if videoFormat:
    for clt in chunklists:
        if clt[1][1] == int(videoFormat):
            chunklist = clt[0]
            break
else:
    # Pick best quality, by height
    # x = ( url, (width, height) )
    chunklists.sort(key=lambda x: -x[1][1])
    chunklist = chunklists[0][0]

chunklistUrl = baseUrl + chunklist

# Update the baseUrl
lastSlash = chunklistUrl.rfind('/')
baseUrl   = chunklistUrl[0:lastSlash+1]


## STEP 2 - Download video files ##
data = urllib2.urlopen(chunklistUrl)


for line in data:
    if( line[0] != '#' ):
        print( baseUrl + line[:-1] )

