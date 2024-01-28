import pymysql
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from db_query_list import get_site_codes
import os 

# initialise pymysql connection
#conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", db="air")





def create_plot_for_site(table, date, pollutant):

    conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", db="air")

    with conn.cursor() as cur:

        sql = "SELECT `time`, `" + pollutant + "` FROM `" + table + "` WHERE `date` = %s;" 
        cur.execute(sql, args = (date, )) # condense formatting into one type?
        request = cur.fetchall


    times = []
    readings = []

# check if record found for pollutant, populate list of axis labels, verify that records exist.
    pollutant_record_found = False
    for record in cur:
        if not record[-1] is None: ###       indexing here
            times.append(record[-2]) ###             may be
            readings.append(float(record[-1])) ###     fubar
            pollutant_record_found = True
            
    if pollutant_record_found:
        # matplotlib plot config/format
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(111)
        plt.plot(times, readings, color='r', linestyle='--', label='pollution', marker='o')
        plt.title(f'{table} readings for {pollutant} on {date}')
        plt.xlabel('time')
        plt.ylabel('reading')
        plt.gcf().autofmt_xdate()
        for r, txt in enumerate(readings):
            ax.text(times[r], readings[r], txt)    
        plt.legend()

        # show plot

        path = f"{table}{pollutant}{date}"
        plt.savefig(f'D:/tom/code/python/tomsite/images/{path}.png')
        return path
        
        

    else:
        print("there are no records for that pollutant in this table")    

    conn.close()


# define visualizer function. needs to query mysql db with table/date/pollutant info.
def show_plotter(table, date, pollutant):  

    conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", db="air")

    with conn.cursor() as cur:
        try:
            sql = "SELECT `time`, `" + pollutant + "` FROM `" + table + "` WHERE `date` = %s;" 
            cur.execute(sql, args = (date, )) # condense formatting into one type?
            request = cur.fetchall
        except:
            print("something went wrong. try again.")
            acquire_inputs()

    times = []
    readings = []

# check if record found for pollutant, populate list of axis labels, verify that records exist.
    pollutant_record_found = False
    for record in cur:
        if not record[-1] is None: ###       indexing here
            times.append(record[-2]) ###             may be
            readings.append(float(record[-1])) ###     fubar
            pollutant_record_found = True
            
    if pollutant_record_found:
        # matplotlib plot config/format
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(111)
        plt.plot(times, readings, color='r', linestyle='--', label='pollution', marker='o')
        plt.title(f'{table} readings for {pollutant} on {date}')
        plt.xlabel('time')
        plt.ylabel('reading')
        plt.gcf().autofmt_xdate()
        for r, txt in enumerate(readings):
            ax.text(times[r], readings[r], txt)    
        plt.legend()

        # show plot
        # plt.show()

        return plt.show()


    else:
        print("there are no records for that pollutant in this table")        



# gather information for plot parameters. site, year, day_month, pollutant.
def acquire_inputs():

    site_codes = [code.lower() for code in get_site_codes()]
    print(site_codes)

    site = input("enter site like 'mahg' \n >>>")
    year = input("enter year like '2023' \n >>>")
    day_month = input("enter date like 'DD-MM' \n >>>")
    pollutant = input("select pollutant by entering corresponding key/typing name \n >>>")

    # call plot function after constructing plot parameters. table, date, pollutant.
    table = site + year
    date = day_month + "-" + year
    show_plotter(table, date, pollutant)



#acquire_inputs()

#plotter("acth2022", "11-05-2022", "Ozone")

# close pymysql connection
#conn.close()