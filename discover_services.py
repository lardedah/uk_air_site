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




{'id': '5116', 'label': 'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/9 9912 - Hafod-yr-ynys Hill Roadside-Nitrogen oxides (air), Hafod-yr-ynys Hill Roadside-Nitrogen oxides (air)', 'uom': 'ug.m-3', 'station': 
{'properties': 
{'id': 787424, 'label': 'Hafod-yr-ynys Hill Roadside-Nitrogen oxides (air)'}, 'geometry': {'coordinates': 
[51.680493, -3.1343249998968368, 'NaN'], 'type': 'Point'}, 'type': 'Feature'}},

