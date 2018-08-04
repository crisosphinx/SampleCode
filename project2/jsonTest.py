import os
import sys
import json


# JSON test

data = {'a list': [1, 42, 3.141, 1337, 'help', u'4'],
        'a string': 'bla',
        'another dict': {'foo': 'bar',
                         'key': 'value',
                         'the answer': 42}}

filN1 = 'Pointer.js'
date1 = '06/06/2017'
date2 = '06/07/2017'

print("File Name: '{}'".format(filN1))
print("Date Uploaded: '{}'".format(date1))
print("Date Updated: '{}'".format(date2))
notes = raw_input("Notes: ")

data = {'File Name: ' : filN1,
        'Date Uploaded: ' : date1,
        'Date Updated: ' : date2,
        'Notes: ' : notes}

dir = ( os.getcwd() + "\\" )
if 'Python' in dir or 'npp' in dir:
    dir = ( "D:\\LocalData\\X094656\\Desktop\\" )

write = raw_input("y/n: ")

if write == 'y':
    with open(dir + "jsonTest.json", 'w') as outfile:
        json.dump(data, outfile)

else:
    with open(dir + "jsonTest.json", 'r') as infile:
        jsonFile = json.load(infile)
        print(jsonFile)
        raw_input()
        