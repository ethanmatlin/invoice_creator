import csv
import time
import argparse
import pandas as pd
import numpy as np

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

    dictionary = {}
    #valueArr = [[0 for x in range(1)] for y in range(data_arr.shape[1])]
    #print(valueArr)
    #valueArr = [[]]

    for i in range(0, len(data_arr)):
        entry = data_arr[i][0:3] + data_arr[i][4:9]
        if data_arr[i][3] in dictionary.keys():
            dictionary[data_arr[i][3]] = dictionary[data_arr[i][3]] + [entry]
        else:
            dictionary[data_arr[i][3]] = [entry]

    print(dictionary)
    print("a")
    for key in dictionary.keys():
        print(key)
        print(dictionary[key])
        print("a")
        print(dictionary[key][len(dictionary[key])-1][0])
        miles = [dictionary[key][j][1]-dictionary[key][j][0] for j in range(0,len(dictionary[key]))]
        hours = [dictionary[key][j][2] for j in range(0,len(dictionary[key]))]
        print(miles)
        print(hours)
        print(miles[len(dictionary[key])-1])
        print(len(dictionary[key][0]))
        tripCharge =[getCharge(miles[j],hours[j],dictionary[key][j][7],dictionary[key][j][6]) for j in range(0,len(dictionary[key])-1)]
        description = [dictionary[key][j][4] for j in range(0,len(dictionary[key])-1)]
        tripDate = [dictionary[key][j][5] for j in range(0,len(dictionary[key])-1)]

    print(dictionary)

    with open("template.txt","r") as f:
        tex_template = f.read().replace('\n','')

    for key in dictionary.keys():
        print(key)
        parser = argparse.ArgumentParser()
        parser.add_argument(invoice, '--invoice')
        parser.add_argument(date, '--currentDate')
        parser.add_argument(key, '--name')


        parser.add_argument(passin, '--data_body')
        parser.add_argument(passin, '--totalcharge')
    args = parser.parse_args()

    cmd = ['pdflatex', filenamehere]
    with open(filenamehere, 'w') as f:
        f.write(content%args.__dict__)
    proc = subprocss.Popen()
    proc.communicate()

    retcode = proc.returncode
    if not retcode==0:
        os.unlink(filenamehere)
        raise ValueError('Error {} executing command: {}:'.format(retcode,' '.join(cmd)))
    os.unlink(filename.tex)
    os.unlink(filname.log)
    #%(date0) & %(miles0) & %(hours0) & %(dest0) & %(charge0) \\
#    %(date0) & %(miles1) & %(hours1) & %(dest1) & %(charge1) \\
 #   %(date0) & %(miles2) & %(hours2) & %(dest2) & %(charge2) \\
  #  %(date0) & %(miles3) & %(hours3) & %(dest3) & %(charge3) \\

main()
