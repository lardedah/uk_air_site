import requests
import cherrypy
import pymysql





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

return_station_id_list()