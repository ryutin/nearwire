#!/usr/bin/env python3

import requests
import json
import sys
import os
import re
import mysql.connector
import datetime
from datetime import datetime, date, time

cnx = mysql.connector.connect(user='rw_user', password='3br!',
                                 host='nearwire-db-instance.cm2yqrbvmu6t.us-east-1.rds.amazonaws.com',
                                 database='nearwire_db')

cursor = cnx.cursor()
#################################
###  BEGIN convert_zulu_date  ###
#################################

def convert_zulu_date(zulu_date):
    """ returns the zulu date in mysql datetime iso8601 format"""
    #       "published": "2018-01-22T23:25:00.000+02:00",
    #print ("zulu:%s",zulu_date)
    clean_datetime = re.search(r'^(\d\d\d\d-\d\d-\d\d)T(\d\d\:\d\d\:\d\d)',zulu_date)
    date = clean_datetime.group(1)
    time = clean_datetime.group(2)
    mysql_datetime = date + ' ' + time
    return (mysql_datetime)

#################################
###  END convert_zulu_date  #####
#################################


#zulu_date = "2018-01-22T23:25:00.000+02:00"
#print ("date:%s",convert_zulu_date(zulu_date))

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
headers = {'user-agent': 'nearwire/0.0.1'}

x = 0
results_available = 1
next_url = ''

r = requests.get('http://webhose.io/filterWebContent', params=userdata, headers=headers)

json_file = open('chicago-il.json','w')

pull_datetime = datetime.utcnow()

add_news_result_blob = (
    "INSERT INTO news_result_blob (part_id,pull_datetime,webhose_json, location, state) "
               "VALUES (%s, %s, %s, %s, %s)"
)

add_news_result_item = (
    "INSERT INTO news_result_item (news_result_blob_id,request_counter,webhose_uuid,domain_name,host_name,article_url,article_title,article_text,publish_datetime,webhose_json) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
)


part_id=0;

while results_available>0 :

    part_id +=1
    if  x>0 :
        r = requests.get('http://webhose.io/'+next_url)

    #print(r.url)
    #print(r.text)
    data = json.loads(r.text)

    json_file.write(r.text)

    next_url = data['next']
    results_available = data['moreResultsAvailable']
    requests_left = data['requestsLeft']

    # INSERT INTO news_result_blob(part_id,pull_datetime,webhose_json, location, state)
    # VALUES(part_id,datetime_now,r.text,city, state)

    #add_employee = ("INSERT INTO employees "
    #           "(first_name, last_name, hire_date, gender, birth_date) "
    #           "VALUES (%s, %s, %s, %s, %s)")
    # data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

    #     "INSERT INTO news_result_blob (part_id,pull_datetime,webhose_json, location, state) "
    #          "VALUES (%s, %s, %s, %s, %s)")


    print("new_result_blob  part_id:%s pull_datetime:%s city:%s state:%s" % (part_id,pull_datetime,city,state))
    news_result_data = (part_id,pull_datetime,r.text,city,state)
    cursor.execute(add_news_result_blob,news_result_data)
    cnx.commit()

    for d in data['posts']:
        x +=1
        webhose_uuid          = d['thread']['uuid']
        article_title         = d['thread']['title']
        domain_name           = d['thread']['site']
        host_name             = d['thread']['site_full']
        article_url           = d['url']
        publish_datetime      = convert_zulu_date(d['thread']['published'])
        article_text          = d['text']
        item_json             = json.dumps(d)

        #print("new_result_item:%04d uuid:%s title:%s domain:%s host:%s ztime:%s ptime:%s" % (x,uuid,title,domain_name,host_name,raw_publish_datetime,zulu_datetime))

        #     "INSERT INTO news_result_item (request_counter,webhose_uuid,domain_name,host_name,article_url,article_title,article_text,publish_datetime,webhose_json) "
        #"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s"

        news_result_item_data = (part_id,x,webhose_uuid,domain_name,host_name,article_url,article_title,article_text,publish_datetime,item_json)
        cursor.execute(add_news_result_item,news_result_item_data)

        cnx.commit()
    print("results_available:" + str(results_available) + " requests_left:" + str(requests_left))
    print("next_url:" + next_url)



#   sys.exit(0)
cursor.close()
cnx.close()
