import csv
import requests
import pymysql
import urllib.request
from urllib.request import urlopen
from io import StringIO
import cherrypy
import os
import scrapy
import re
from bs4 import BeautifulSoup
from db_query_list import *
import time


def return_coords(station_id):

    conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", db="air")
    cur = conn.cursor()

    sql = f"select coord0, coord1 from stations WHERE station_id = {station_id}"
    
    cur.execute(sql)

    data_tuple = cur.fetchall()
    row = data_tuple[0]
    coord0 = row[0]
    coord1 = row[1]

    return coord0, coord1

    cur.close()
    conn.close()





def return_station_id_list():
    conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", db="air")
    cur = conn.cursor()

    sql = f"SELECT station_id FROM stations"
    
    cur.execute(sql)

    data = cur.fetchall()

    list_of_station_ids = []

    for each_tuple in data:
        list_of_station_ids.append(each_tuple[0])

    return list_of_station_ids

    cur.close()
    conn.close()






def get_site_codes():

    conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", db="air")
    cur = conn.cursor()

    base_url = 'https://uk-air.defra.gov.uk/latest/currentlevels?view=region'
    base_station_url = 'https://uk-air.defra.gov.uk/data/flat_files?site_id='

    htmla = urlopen(base_url)
    bsobj = BeautifulSoup(htmla.read())

    page_links = [link.get(str('href')) for link in bsobj.find_all('a', href=re.compile("site-info?"))]

    codes = [] # init empty list, will be list of 2-4 character strings
    
    for pagelink in page_links: # maybe consolidate following chunk of code down, using comprehension?

        composite_tail = []
        for character in pagelink:
            if character.isupper() or character.isnumeric(): # awkward. but it works, for now.
                composite_tail.append(character)
            else:
                pass
        code = ''.join(composite_tail)
        codes.append(code) # codes is now list of 2-4 character strings

    return codes

    cur.close()
    conn.close()


    #print(codes.index("")) # in case of 504. use this to find index of station.
    #return codes[:46] # in case of 504, use this to avoid completed stations.
# get_station_codes() # in case of 504. use this to run above function.