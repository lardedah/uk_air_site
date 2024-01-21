import requests
import cherrypy
import pymysql

conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", db="air")
cur = conn.cursor()
    
for r in range(1, 1000000):

    response = requests.get( "https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries/")
    data = response.json()

    for d in data:
        print(d[1])

    cur.execute
    conn.commit

cur.close()
conn.close()