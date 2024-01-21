import requests
import cherrypy
import pymysql
import os
from db_query_list import *


station_list = return_station_id_list()

with open("D:/tom/code/python/tomsite/station_list.txt", 'w') as file:

    for s in station_list:

        file.write(str(s) + "\n")