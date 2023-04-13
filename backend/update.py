import requests
import csv

'''
address = []
private_key = []
mycsv = csv.reader(open('csv/address.csv'))
for row in mycsv:
   address.append(row[0])
  
mycsv2 = csv.reader(open('csv/private_key.csv'))
for row in mycsv2:
   private_key.append(row[0])

print(private_key[0])


int = -1
mycsv3 = csv.reader(open('csv/thousand_names.csv'))
for row in mycsv3:
   int += 1
   print(private_key[int])
   data = {
        'username':row[0],
        'address':address[int],    
        'private_key': private_key[int],   
        }
   object = requests.post("http://127.0.0.1:8000/api/v1/updateAccount/", json=data)

'''


energy = [10,95,20,85,30,75,40,65,50,55]
int = 5089
is_on = True
for i in range(5425):
   data = {
      'id':int,
      'is_on':is_on,
   }
   object = requests.post("http://127.0.0.1:8000/api/v1/updateObject/", json=data)
   int +=1
