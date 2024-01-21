import requests
import cherrypy
import pymysql
import js.leaflet
from db_query_list import *


conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", db="air")
cur = conn.cursor()


class site(object):
    

    @cherrypy.expose
    def index(self):


        return """<html>
          <body>
          <h>tomsite</h>
          <style>
          body {background-color: powderblue;}
          </style>
          <form method="get" action="stations">
          <button type="submit">stations</button>
          <p>test</p>
          </body>
        </html>"""
    

    @cherrypy.expose
    def stations(self, station=0):
        station = int(station) 


        if station > 0:
 

            sql = "SELECT stations.label, stations.category_id, categories.url FROM stations INNER JOIN categories on stations.category_id = categories.category_id WHERE stations.station_id = %s;"
            cur.execute(sql, (str(station)))
            data = cur.fetchall() 


            station_label = data[0][0]
            category_id = data[0][1]
            category_url = data[0][2]


            station_coord_tuple = return_coords(station)
            a = str(station_coord_tuple[0])
            b = str(station_coord_tuple[1])


            return ''.join(f'station {station}: longitude = ' + a + ' ' + 'latitude = ' + b) + """<html> 

            <head>

            <style>

            body {background-color: powderblue;}

            #map { height: 675px; width: 1200px}

            </style>

            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
            integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
            crossorigin=""/>

            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
            integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
            crossorigin=""></script>

            </head>

            <body>

            <div id="map"></div>

            <script>

            """ + f"""
            var map = L.map('map').setView([{a}, {b}], 16);
            """ + """

            const attribution = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>' 
            }).addTo(map);

            """ + f"""
            const marker = L.marker([{a}, {b}]).addTo(map);

            marker.bindPopup("<b>{station_label}</b><br>EIONET pollutant category {category_id} @  <a href='{category_url}' target = '_blank'>(new page)</a> ").openPopup();

            """ + """
            
            tiles.addTo(map);

            </script>

            <form method="get" action="stations">
            <button type="submit">stations</button>

            </body>

            </html>"""






        else:


            station_id_list = return_station_id_list()


            html = """<html>
                <body>
                <style>
                body {background-color: powderblue;}
                </style>
                <form method="get" action="index">
                <button type="submit">home</button>"""       
    

            for station in station_id_list:
                
                sql = 'SELECT label FROM stations WHERE station_id = %s'

                cur.execute(sql, station)
                data = cur.fetchall()

                station_label = data[0][0]

                html = html + f"""
                                <li><a href="?station={station}"> view station id {station}........'{station_label}' </a></li>
                            """


            html = html + """</body>
                    </html>"""


            return html









if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
        },
        }
    cherrypy.quickstart(site(), '/', conf)


cur.close()
conn.close()