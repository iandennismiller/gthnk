#!/usr/bin/env python

# http://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time, json

lists = {}

#######
# ideas
with open("/Users/idm/Library/Journal/lists/ideas.txt", "r") as i:
    ideas = list(line.strip() for line in i.readlines() if line.strip())
    ideas.reverse()
lists["ideas"] = ideas

#######
# themes
with open("/Users/idm/Library/Journal/lists/themes.txt", "r") as i:
    themes = list(line.strip() for line in i.readlines() if line.strip())
    themes.reverse()
lists["themes"] = themes

#######
# media
with open("/Users/idm/Library/Journal/lists/media.txt", "r") as i:
    media = list(line.strip() for line in i.readlines() if line.strip())
    media.reverse()
lists["media"] = media

#######
# radar
with open("/Users/idm/Library/Journal/lists/radar.txt", "r") as i:
    radar = list(line.strip() for line in i.readlines() if line.strip())
    #radar.reverse()
lists["radar"] = radar

#######
# wanna
with open("/Users/idm/Library/Journal/lists/wanna.txt", "r") as i:
    wanna = list(line.strip() for line in i.readlines() if line.strip())
    wanna.reverse()
lists["wanna"] = wanna

#######
# export it all
with open('/tmp/lists.json', 'w') as f:
    buf = "var lists = " + json.dumps(lists, indent=4)
    f.write(buf)
