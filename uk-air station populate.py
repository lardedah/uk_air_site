import requests
import cherrypy
import pymysql

root_url = 'https://uk-air.defra.gov.uk/sos-ukair/api/v1'
services_tail = '/services'
categories_tail = '/categories'
phenomena_tail = '/phenomena'
stations_tail = '/stations'

conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", db="air")
cur = conn.cursor()

response = requests.get(f"{root_url}{stations_tail}")
data = response.json()

fails = []

for d in data:
    
    if 'geometry' in d and 'properties' in d:

        properties = d['properties']
        for p in properties:
            id = properties['id']
            label = properties['label']

        geometry = d['geometry']
        for g in geometry:
            coordinates = geometry['coordinates']
            for c in coordinates:
                coord0 = coordinates [0]
                coord1 = coordinates [1]

        info = []
        info.append(id)
        info.append(label)
        info.append(coord0)
        info.append(coord1)

        sql = f'INSERT INTO stations (station_id, label, coord0, coord1) VALUES (%s, %s, %s, %s)'

        cur.execute(sql, args = info)
        conn.commit()

    else:
        fails.append(d)

cur.close()
conn.close()

print(f"fails: {fails}")