# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 17:04:28 2016
@author: Andreas Drotth, Sebastian Olsson, TODO: FILL IN OTHERS
"""
from scipy import *
from pylab import *
from datetime import datetime
from datetime import timedelta
import pytz
from preprocess import preprocessing

list_dates = []
list_data = []
converted_dates = []
plot_dates = []
plot_data = []

# --------------------- TASK 2 ------------------------------------------------


def convert_local_timezone():

    for date in list_dates:
        local_tz = pytz.timezone('Europe/Stockholm')
        local_time = date.replace(tzinfo=pytz.utc).astimezone(local_tz)
        converted_dates.append(local_time)


# --------------------- TASK 4 ------------------------------------------------


def compute_data():
    #start_date = input('Start date [YYYY-MM-DD]: ')
    #days = input('Number of days: ')  
    
    checkstartdate=True
    while(checkstartdate):
        try:
            start_date = input('Start date [YYYY-MM-DD]: ')
            datelist = start_date.split('-')
            datetime(year=int(datelist[0]), month=int(datelist[1]),day=int(datelist[2]))
            checkstartdate=False
        except:
            print("You have to write input on the form YYYY-MM-DD")      
    
    checkinterval=True        
    while(checkinterval):
        try:
            days = int(input('Number of days: '))
            checkinterval=False
        except ValueError:
            print("You have to write an integer")
     
    date_1 = datetime.strptime(start_date, "%Y-%m-%d")

    collect_plot_dates(start_date)  # collect dates/data for start date

    if int(days) > 1:  # Repeat collection for each plus day separatly
        for t in range(1, int(days)):
            end_date = date_1 + timedelta(int(t))
            a, b = str(end_date).split()
            collect_plot_dates(a)

    array1 = np.array(plot_data)
    diff_array = np.diff(array1)
    graph_dates, graph_data = graph_values(diff_array)

    return graph_dates, graph_data


def collect_plot_dates(start_date):
    first = 0
    last = 0
    index_list = []

    for i in list_dates:
        if (start_date in str(i)):
            index_list.append(list_dates.index(i))
            plot_dates.append(i)

    first = index_list[0]
    last = index_list[-1]
    collect_plot_data(first, last)


def collect_plot_data(first, last):
    for k in range(first, last+1):
        plot_data.append(int(list_data[k]))


def graph_values(diff_array):
    graph_data = []
    graph_dates = []
    sum_value = 0
    index = 0
    current_hour = plot_dates[0].hour
    
    graph_dates.append(plot_dates[0].strftime('%Y-%m-%d %H:%M:%S'))
    
    for data in diff_array:
        if (plot_dates[index].hour > current_hour):
            graph_data.append(sum_value)
            sum_value = 0
            sum_value = sum_value + int(data)
            current_hour = current_hour + 1
            graph_dates.append(plot_dates[index].strftime('%Y-%m-%d %H:%M:%S'))
        elif (plot_dates[index].hour < current_hour):
            graph_data.append(sum_value)
            sum_value = 0
            sum_value = sum_value + int(data)
            current_hour = 0
            graph_dates.append(plot_dates[index].strftime('%Y-%m-%d %H:%M:%S'))
        else:
            sum_value = sum_value + int(data)
        
        index = index + 1
    
    graph_data.append(sum_value)

return graph_dates, graph_data

# --------------------- TASK 5 ------------------------------------------------


def plot_graph(graph_dates, graph_data):
    x_values=[]
    for i in graph_dates:
        x_values.append(datetime.strptime(i, '%Y-%m-%d %H:%M:%S'))
    
    y_values = np.array(graph_data)


    fig = plt.figure()
    
    ax = fig.add_subplot(111)
    barWidth = 1.0/(len(x) + 2)
    ax.bar(x_values, y_values, width=barWidth , color='green', align='center')
    
    plt.gcf().autofmt_xdate()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    ax = plt.gca()
    
    
    xaxis = ax.get_xaxis()
    xaxis.set_major_locator(dates.DayLocator())
    xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))

    space=3
    start=2
    end=24
    
    hours=int((x_values[-1]-x_values[0]).total_seconds()/3600)+1
    if(hours>96):
        space=5
    
    xaxis.set_minor_locator(dates.HourLocator(byhour=range(start,end,space)))
    xaxis.set_minor_formatter(dates.DateFormatter('%H'))#minor locator timme
    xaxis.set_tick_params(which='major', pad=18) #sätter ner datumen med 18 steg
    
    plt.title("Nesting box activities")
    plt.ylabel("In/out movements per hour")
    save_plot()
    plt.show()

# --------------------- TASK 6 ------------------------------------------------


def day_night_cycle():
    print("Visualize day and night cycle")

# --------------------- TASK 7 ------------------------------------------------
def save_plot():
    save = input('Press s to save graph as png file or enter to skip: ')
    if(save=='s'):
        plt.savefig('bird_movements.png',bbox_inches='tight')
        print("File saved as bird_movements.png in your working directory")

if __name__ == '__main__':
    list_dates, list_data = preprocessing("birds.txt")
    convert_local_timezone()
    graph_dates, graph_data = compute_data()
    plot_graph(graph_dates, graph_data)
    # day_night_cycle()
