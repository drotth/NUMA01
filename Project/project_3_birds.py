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
    start_date = input('Start date [YYYY-MM-DD]: ')
    days = input('Number of days: ')
    date_1 = datetime.strptime(start_date, "%Y-%m-%d")

    collect_plot_dates(start_date)  # collect dates/data for start date
    # collect_plot_dates2(start_date, days)

    if int(days) > 1:  # Repeat collection for each plus day separatly
        for t in range(1, int(days)):
            end_date = date_1 + timedelta(int(t))
            a, b = str(end_date).split()
            collect_plot_dates(a)

    array1 = np.array(plot_data)
    diff_array = np.diff(array1)
    graph_dates, graph_data = graph_values(diff_array)

    return graph_dates, graph_data


def collect_plot_dates2(start_date, days):
    first = 0
    last = 0
    index_list = []
    date_found = False
    
    date_1 = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = date_1 + timedelta(int(days))

#    for i in list_dates:
#        if (start_date in str(i)):
#            index_list.append(list_dates.index(i))

    for i in list_dates:
        a, b = str(i).split()
        
        if (date_found == False and start_date in a):
            # print("FOUND IT AT INDEX:", list_dates.index(i))
            date_found = True
            plot_dates.append(i)
            first = list_dates.index(i)
        elif(date_found == True):
            # print("APPENDING INDEX:", list_dates.index(i))
            plot_dates.append(i)
            if (end_date.strftime('%Y-%m-%d') in a):
                # print("STOPPING AT INDEX:", list_dates.index(i))
                last = list_dates.index(i)
                break
        last = list_dates.index(i)

    # first = index_list[0]
    # last = index_list[-1]

    print("first is:", first)
    print("last is:", last)    
    
    collect_plot_data(first, last)


def collect_plot_dates(start_date):
    first = 0
    last = 0
    index_list = []

    for i in list_dates:
        if (start_date in str(i)):
            index_list.append(list_dates.index(i))

    for i in list_dates:
        a, b = str(i).split()
        if (start_date in a):
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

    graph_dates.append(plot_dates[0].strftime('%Y-%m-%d'))

    print("Length of diff_array", len(diff_array))
    print("Length of plot_dates", len(plot_dates))
    print("Length of plot_data", len(plot_data))

    for data in diff_array:
        if (plot_dates[index].hour > current_hour):
            graph_data.append(sum_value)
            sum_value = 0
            sum_value = sum_value + int(data)
            current_hour = current_hour + 1
            graph_dates.append(str(current_hour))
        elif (plot_dates[index].hour < current_hour):
            graph_data.append(sum_value)
            sum_value = 0
            sum_value = sum_value + int(data)
            current_hour = 0
            graph_dates.append(plot_dates[index].strftime('%Y-%m-%d'))
        else:
            sum_value = sum_value + int(data)

        index = index + 1

    graph_data.append(sum_value)

    return graph_dates, graph_data

# --------------------- TASK 5 ------------------------------------------------


def plot_graph(graph_dates, graph_data):
    x_values = np.array(range(0, len(graph_dates)))
    y_values = np.array(graph_data)
    x_names = graph_dates
    print(x_names)

    ax = plt.subplot(111)
    plt.xticks(rotation=90)  # Roterar det som står på x-axeln
    plt.xticks(x_values, x_names)
    barWidth = 1  # Bredd på staplarna
    ax.bar(x_values, y_values, width=barWidth, align='center')
    plt.show()

# --------------------- TASK 6 ------------------------------------------------


def day_night_cycle():
    print("Visualize day and night cycle")

if __name__ == '__main__':
    list_dates, list_data = preprocessing("birds.txt")
    convert_local_timezone()
    graph_dates, graph_data = compute_data()
    plot_graph(graph_dates, graph_data)
    # day_night_cycle()
