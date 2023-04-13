import requests
import csv

mycsv = csv.reader(open('thousand_names.csv'))
for row in mycsv:
   print(row[0])
   data = {
        'username':row[0],       
        }
   object = requests.post("http://127.0.0.1:8000/api/v1/deleteTest/", json=data)
   print(object.json())