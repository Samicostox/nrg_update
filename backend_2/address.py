import requests
import csv

'''
mycsv = csv.reader(open('address.csv'))
for row in mycsv:
    new = row[0].split()
    print(new[1])
    with open('new_address.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow([new[1]])
'''

mycsv = csv.reader(open('private_key.csv'))
for row in mycsv:
    new = row[0].split()
    print(new[1])