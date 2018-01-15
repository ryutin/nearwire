#!/usr/local/bin/python3

import requests
import json
import sys
import os

# http://webhose.io/filterWebContent?
# token=API_KEY
# format=json&
# sort=crawled&
# q=location%3Achicago%20
## location%3Aillinois%20
## site_type%3Anews%20
## language%3Aenglish%20
## thread.country%3AUS

API_KEY=os.getenv("WEBHOSE_APIKEY")


city      = 'chicago'
state     = 'illinois'
site_type = 'news'
language  = 'english'
country   = 'US'

location_string = 'location:%s location:%s site_type:%s language:%s thread.country:%s' % (state,city,site_type,language,country)
#print("api_key:",API_KEY)
#sys.exit(0)

userdata = {'token':API_KEY,'format':'json','sort':'crawled','q':[location_string]}
headers = {'user-agent': 'nookie/0.0.1'}

x = 0
results_available = 1
next_url = ''

r = requests.get('http://webhose.io/filterWebContent', params=userdata, headers=headers)

json_file = open('chicago-il.json','w')

while results_available>0 :

    if  x>0 :
        r = requests.get('http://webhose.io/'+next_url)

    #print(r.url)
    #print(r.text)
    data = json.loads(r.text)

    json_file.write(r.text)

    next_url = data['next']
    results_available = data['moreResultsAvailable']
    requests_left = data['requestsLeft']

    for d in data['posts']:
        x = x+1
        uuid =d['thread']['uuid']
        title = d['thread']['title']
        print("%04d uuid:%self title:%s" % (x,uuid,title))

    print("results_available:" + str(results_available) + " requests_left:" + str(requests_left))
    print("next_url:" + next_url)
#    if x>100 :
#        sys.exit(0)
