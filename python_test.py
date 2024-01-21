from urllib.request import urlopen
from io import StringIO
import csv
import time

#conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", db="air")



with urlopen("https://uk-air.defra.gov.uk/data_files/site_data/MAHG_2023.csv?v=1") as resource:
    content = resource.read().decode('ascii', 'ignore')
    file = StringIO(content)

next(file)
next(file)
next(file)
next(file)

dictReader = csv.DictReader(file, dialect='excel')

for row in dictReader:
    print(row)
    break
