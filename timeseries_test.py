import requests
import cherrypy
import pymysql
import js.leaflet
from db_query_list import *

conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", db="air")
cur = conn.cursor()


response = requests.get(f"https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries/")
data = response.json()


print(data)














cur.close()
conn.close()