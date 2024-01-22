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


def get_station_codes():

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
    #return codes[148:] # returns COAL onwards.


def year_truncate_all_tables(year):

    station_codes = get_station_codes()
    for code in station_codes:
        sql = f"TRUNCATE TABLE `{code}{year}`"
        print(sql)
        cur.execute(sql)
        conn.commit()


def get_column_labels(csv_link, station_code):

    with urlopen(csv_link) as resource:
        content = resource.read().decode('ascii', 'ignore')
        file = StringIO(content)

        next(file) # high-skill coding
        next(file) #
        next(file) #
        next(file) # 

        dictReader = csv.DictReader(file, dialect='excel') # dialect is default excel

        column_labels = [station_code]

        for row in dictReader:
            for key in row.keys():
                key = key.replace(",", " ")
                column_labels.append(key)         
            break
        return column_labels


def create_table(year): 

    base_url = 'https://uk-air.defra.gov.uk/latest/currentlevels?view=region'
    base_station_url = 'https://uk-air.defra.gov.uk/data/flat_files?site_id='

    year = str(year) # if not str, then now str.
    station_codes = get_station_codes()
    for station_code in station_codes: # return object is a list of 2-4 character strings.

        page_url = base_station_url + station_code
        htmlb = urlopen(page_url)
        bsobj = BeautifulSoup(htmlb.read()) # page url as bs obj.
        
        string = (f'{station_code}_{year}') # I think this can go go gadget.

        csv_bsobj = bsobj.find('a', href=re.compile('.*({}).*'.format(year))) # find, not findall, because the year in general is in first table of links.

        if not csv_bsobj == None:
            print("doing something")

            csv_link = csv_bsobj.get('href') # url from href tag. the first eligible link on each page is the year's hourly data.

            with urlopen(csv_link) as resource:
                column_labels = [station_code]
                column_labels = get_column_labels(csv_link, station_code)
                
                arg_counter = 0

                sql = "CREATE TABLE IF NOT EXISTS `" + column_labels[0] + year + "`("

                for label in range((len(column_labels) -2)):                                            # can change f strings over to concatenation. or not. reduce methods used and improve this sql construction loop.
                    sql = sql + f"`{column_labels[(arg_counter + 1)]}` varchar(150), "
                    arg_counter += 1
                print(station_code) # show code before sql execute
                print(sql) # show full sql before sql execute
                sql = sql + f"`{column_labels[-1]}` varchar(150));" 

                cur.execute(sql)  

        else:
            pass # I want to end for loop. this will progess script to next code in for loop @ line 45.


def populate_tables(year):

    base_url = 'https://uk-air.defra.gov.uk/latest/currentlevels?view=region'
    base_station_url = 'https://uk-air.defra.gov.uk/data/flat_files?site_id='

    year = str(year) # if not str, then str.
    station_codes = get_station_codes()
    for station_code in station_codes: # return object is a list of 2-4 character strings.

        # IF EXISTS? SOME STATION CODES DON'T HAVE ALL YEAR'S DATA FILES. I THINK LINE 142 SHOULD DO THIS. LET'S SEE.

        page_url = base_station_url + station_code
        htmlb = urlopen(page_url)
        bsobj = BeautifulSoup(htmlb.read()) # page url as bs obj.
        
        string = (f'{station_code}_{year}') # I just changed the hard-coded '2023' to {year}. I believe this will work.

        csv_bsobj = bsobj.find('a', href=re.compile('.*({}).*'.format(year))) # find, not findall, because the year in general is in first table of links.

        if not csv_bsobj == None: # checks for None type returned in the case of no results found by .find

            csv_link = csv_bsobj.get('href') # url from href tag. the first eligible link on each station page is the year's hourly data.
            
            with urlopen(csv_link) as resource: # csv file is now open.
                               
                content = resource.read().decode('ascii', 'ignore')
                file = StringIO(content)

                next(file) # high-skill coding
                next(file) #
                next(file) #
                next(file) #

                dictReader = csv.DictReader(file, dialect='excel')
                next(dictReader)

                for row in dictReader: # for row(dict) in table

                    # following mess is to prep column/value for sql query.
                    raw_columns = []
                    clean_column_constructor = []
                    clean_columns = []
                    raw_values = []
                    clean_values = []
                  
                    for k in row: # (row is dict type, so this looks at keys and values are then indexed from this)
                        if row[k] == "":
                            raw_columns.append(k)
                            raw_values.append("NULL")
                        else:                         
                            raw_columns.append(k)
                            raw_values.append(row[k])
                    
                    # following for loops may be able to be integrated into the above chunk.

                    for raw_column in raw_columns:                        
                        clean_column_constructor.append(raw_column.replace(",", " ")) # replace commas with ' ' because sql delimiter
                       
                    for raw_column in clean_column_constructor:
                        clean_columns.append(raw_column.center((len(raw_column) +2), "`"))
                    
                    for raw_value in raw_values:
                        if raw_value == "NULL":
                            clean_values.append(raw_value)
                        elif ":" in raw_value:
                            almost = raw_value.replace(":", ".")
                            clean_values.append(almost.center((len(almost) + 2), "'"))
                        else:
                            clean_values.append(raw_value.center((len(raw_value) + 2), "'"))
                    

                    

                    sql = f"INSERT INTO `{station_code.lower()}{year.lower()}` ({', '.join(clean_columns)}) VALUES ({', '.join(clean_values)});"
                    print(sql)
                    cur.execute(sql)
                    conn.commit()

        else:
            print(".find returned no objects. does it exist?") # I want to end for loop. this will progess script to next code in for loop.


#create_table
for year in range(2000, 2022):
    populate_tables(year)
#year_truncate_all_tables


cur.close()
conn.close()