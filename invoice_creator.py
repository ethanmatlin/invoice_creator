import csv
import time
import os
import argparse
import pandas as pd
import numpy as np
from string import Template
import subprocess
import json

def getCharge(miles, hours, things47, student):
    if student==1:
        if things47==1:
            return 1.5*miles
        elif things47==0:
            return 15*hours+1.5*miles
        else:
            print("Error: 47 things must be 0 or 1")
            return -9999999999
    elif student==0:
        if miles<=50:
            return 40*hours
        else:
            return 30*hours+1.5*miles
    else:
        print("Error: student must be 0 or 1")
        return -999999999


#def nameExist():

def csv_parser(file_path):
    csv_file = open(file_path, 'r')
    dictionary = {}
    with csv_file as data:
        reader = csv.DictReader(data)
        for row in reader:
            dictionary[row[4]] = row['EMAIL']
    return dictionary

def nameExists(dictionary,k):
    for key in dictionary.keys():
        return k==key


def main():
   # path =
    date = time.strftime("%c")
    totalCharge = 0.0
    nameHTML = ""
    with open("invoiceNum.txt") as f:
        data = f.readlines()
    invoice = int(data[0])

    data_path = "~/Downloads/test.csv"
    df = pd.read_csv(data_path, header=None)
    data_arr = (df.as_matrix()).tolist()
    print(data_arr)

    dict = {}
    #valueArr = [[0 for x in range(1)] for y in range(data_arr.shape[1])]
    #print(valueArr)
    #valueArr = [[]]

    for i in range(0, len(data_arr)):
        #entry = data_arr[i][0:3] + data_arr[i][4:9]
        miles = [round(data_arr[i][1]-data_arr[i][0],2)]
        hours = [round(data_arr[i][2],2)]
        tripCharge = [getCharge(miles[0],hours[0],data_arr[i][8], data_arr[i][7])]
        description = [data_arr[i][5]]
        tripDate = [data_arr[i][6]]
        if data_arr[i][3] in dict.keys():
            dict[data_arr[i][3]] = {'miles': dict[data_arr[i][3]]['miles'] + miles,
                                    'hours': dict[data_arr[i][3]]['hours'] + hours,
                                    'tripCharge': dict[data_arr[i][3]]['tripCharge'] + tripCharge,
                                    'description': dict[data_arr[i][3]]['description'] + description,
                                    'tripDate': dict[data_arr[i][3]]['tripDate'] + tripDate
            }
           # dict[data_arr[i][3]] + [entry]
        else:
            dict[data_arr[i][3]] = {'miles': miles,
                                    'hours': hours,
                                    'tripCharge': tripCharge,
                                    'description': description,
                                    'tripDate': tripDate
            }

    print(dict)


    for key in dict.keys():
        total_charge=0
        data_body = ""
        print(dict[key]['miles'])
        for i in range(len(dict[key]['miles'])):
            total_charge = total_charge + dict[key]['tripCharge'][i]
            data_body = data_body + dict[key]['tripDate'][i].replace("/","\//") + "&" + str(dict[key]['miles'][i]) + "&" + str(dict[key]['hours'][i]) + "&" + dict[key]['description'][i] + "&" +  str(dict[key]['tripCharge'][i]) + "\\\ "
        print(data_body)
        template_file = open('template.txt')
        tex = Template(template_file.read().replace('\n',''))
        template_file.close()
        subs = {'invoice': invoice,
                'currentDate': date,
                'name': key,
                'data_body': data_body,
                'totalcharge': total_charge
        }
        tex = tex.substitute(subs)

        filename = key.replace(' ', '')  + str(invoice)

        os.chdir('../')
        cmd = "pdflatex -interaction nonstopmode " + filename +'.tex'
        with open(filename+'.tex', 'w') as f:
            f.write(tex)
            f.close()

        os.system(cmd)

        os.unlink(filename + ".tex")
        os.unlink(filename + ".log")
        os.unlink(filename + ".aux")
        os.chdir('script')
main()
