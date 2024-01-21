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

conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", db="air")
cur = conn.cursor()
# eg csv url https://uk-air.defra.gov.uk/data_files/site_data/MAHG_2023.csv?v=1 # for reference

def create_table(year): 
    year = str(year) # if not str, then str.
    base_url = 'https://uk-air.defra.gov.uk/latest/currentlevels?view=region'
    base_station_url = 'https://uk-air.defra.gov.uk/data/flat_files?site_id='

    htmla = urlopen(base_url)
    bsobj = BeautifulSoup(htmla.read())

    page_links = [link.get(str('href')) for link in bsobj.find_all('a', href=re.compile("site-info?"))]

    codes = [] # init empty list, will be list of 2-4 character strings
    
    for pagelink in page_links: # maybe consolidate this chunk of code down using comprehension.

        composite_tail = []
        for character in pagelink:
            if character.isupper() or character.isnumeric(): # awkward. but it works, for now.
                composite_tail.append(character)
            else:
                pass
        code = ''.join(composite_tail)
        codes.append(code) # codes is now list of 2-4 character strings
    


    for c in codes: # 'codes' is a list of 2-4 character strings.

        page_url = base_station_url + c
        htmlb = urlopen(page_url)
        bsobj = BeautifulSoup(htmlb.read()) # page url as bs obj.
        
        string = (f'{code}_{year}') # I just changed the hard-coded '2023' to {year}. I believe this will work.

        csv_bsobj = bsobj.find('a', href=re.compile('.*({}).*'.format(year))) # find, not findall, because the year in general is in first table of links.
        # these could maybe be one line.

        if not csv_bsobj == None:    

            csv_link = csv_bsobj.get('href') # url from href tag. the first eligible link on each page is the year's hourly data.

            with urlopen(csv_link) as resource:
                content = resource.read().decode('ascii', 'ignore')
                file = StringIO(content)

                next(file) # highly specific to datasets.
                next(file) #
                next(file) #
                next(file) # will probably become an issue at some point.

                dictReader = csv.DictReader(file, dialect='excel')
                
                column_labels = [c]



                for row in dictReader:
                    for key in row.keys():
                        #print(key)
                        key = key.replace(",", " ")
                        #print(key)
                        column_labels.append(key)         
                    break
                


                arg_counter = 0

                sql = "CREATE TABLE IF NOT EXISTS `" + column_labels[0] + year + "`("

                for label in range((len(column_labels) -2)):
                    sql = sql + f"`{column_labels[(arg_counter + 1)]}` varchar(150), "
                    arg_counter += 1
                print(c) # show code before sql execute
                print(sql) # show full sql before sql execute
                #print(column_labels)
                sql = sql + f"`{column_labels[-1]}` varchar(150));" 

                cur.execute(sql)           

        else:
            pass # I want to end for loop. this will progess script to next code in for loop @ line 45.



# create_table()
# populate_table() ?


cur.close()
conn.close()