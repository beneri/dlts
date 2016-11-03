#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import urllib


loginUrl = 'https://www.sats.se/satselixia/webapi/auth/login'
userField = 'UserName'
passField = 'Password'

cred = ('your username','your password')

s = requests.Session()
payload = {userField: cred[0], passField: cred[1]}


# Login
r = s.post(loginUrl, data=payload)

# Get the list of videos
r = s.get('https://www.sats.se/satselixia/webapi/filteredproducts/sv/21155/0')
videos = json.loads( r.text )
i = 0
for video in videos:
    print('['+str(i)+'] ' + video['MediaId'] + ' '  + video['Name'] )
    i = i + 1


# Pick a video
try:
    idn = int( raw_input('video id: ') )
    video = videos[idn]
except:
    print('Bad id!')
    raise

productUrl = 'https://www.sats.se' + video['ProductPageUrl']

# Fetch the page for that video
r = s.get(productUrl)

# Now find the player and authentication credentials for the video
# First 's.src' is for the teaser
start = r.text.find('s.src')
# second is for the real video
start = r.text.find('s.src',start+1)
end = r.text.find('&amp;', start)
playerUrl = r.text[start+12:end]

# Fetch the player code
r = s.get(playerUrl)


# Find the screen9 api json object
pattern = 'screen9.api.embed({'
start = r.text.find(pattern) + len(pattern) - 1
end = r.text.find('})\n')
screen9api = json.loads( r.text[start:end]   )

# Extract the playlist
playlistUrl = screen9api['data']['flash']['playlist'][0]['url']

# Send playlist url to dlts.py
print urllib.unquote(playlistUrl)


