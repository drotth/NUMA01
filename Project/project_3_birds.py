# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 17:04:28 2016
@author: Andreas Drotth, Sebastian Olsson, TODO: FILL IN REST
"""
from scipy import *
from pylab import *
from datetime import datetime  # Biblioteket som claus nämner i uppgiften
import pytz

# --------------------- TASK 1 ------------------------------------------------


def read_file():
    file = open("birds.txt", "r")  # Öppnar filen birds
    listG = []

    for line in file:  # En for-loop som går igenom birds.txt
        # Detta är en formatet för tiden och datumet
        frmt = '%Y-%m-%d %H:%M:%S.%f'
        a, b, c = line.split()  # Delar upp datum, tid och data till a, b och c
        # Lägger till a och b som datetimeobjects i listG
        listG.append(datetime.strptime(a + " " + b, frmt))

# --------------------- TASK 2 ------------------------------------------------


def convert_local_timezone():
    newList = []

    for date in listG:  # Variabeln date går igenom förra listan (listG)
        local_tz = pytz.timezone('Europe/Stockholm')  # Lokal tidszon
        # Variabeln date överförs till den lokala tidszonen
        local_time = date.replace(tzinfo=pytz.utc).astimezone(local_tz)
        newList.append(local_time)  # Lägger till nya tider i den nya listan