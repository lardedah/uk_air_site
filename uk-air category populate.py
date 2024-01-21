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

response = requests.get(f"{root_url}{categories_tail}")
data = response.json()

for d in data:

    id = d['id']

    label = d['label']

    info = []
    info.append(id)
    info.append(label)

    sql = f'INSERT INTO categories (category_id, label) VALUES (%s, %s)'

    cur.execute(sql, args = info)
    conn.commit()

cur.close()
conn.close()