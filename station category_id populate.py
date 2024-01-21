import requests
import cherrypy
import pymysql

url = "https://uk-air.defra.gov.uk/sos-ukair/api/v1/categories?station="
conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", db="air")
cur = conn.cursor()

sql = 'SELECT station_id FROM stations;'
cur.execute(sql)
result = cur.fetchall()

int_station_id_list = []
for id in result:
    int_station_id_list.append(id[0])

for int_station_id in int_station_id_list:

    str_station_id = str(int_station_id)

    response = requests.get(f"{url}{str_station_id}")
    data = response.json()

    for d in data:
        cat_id = d['id']
        cat_id = int(cat_id)

        ssql = f'UPDATE stations SET category_id = {cat_id} WHERE station_id = {int_station_id}' 
        cur.execute(ssql)
        conn.commit()

cur.close()
conn.close()