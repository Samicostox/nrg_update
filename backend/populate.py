import requests
import csv
import bcrypt
import random

appliances = [[[1,1,1,2,2,2,1,1,1,2], ["Fridge","Small Fridge"],"REFREGIRATOR", ["Kitchen","Kitchen"],["Beko CFG1790DB", "Beko CRFG1582W260", "Beko CFG1790DB", "Beko CRFG1582W", "Hotpoint NRFAA50P", "Hotpoint Day 1 SXBHE925WD", "Hotpoint Day 1 SXBHE925WD", "Bosch Serie 4 KGN36IJ3AG", "Bosch Serie 6 KIR81AF30G", "Bosch Serie 4 KGN36IJ3AG"]], 
            [[1,1,1,1,1,1,1,1,0,0],["Washing Machine"],"WASHING_MACHINE", ["Kitchen",], ["Hoover Dynamic Next DXOA69C3", "Hoover H-Wash 500 HW411AMC", "Hoover Dynamic Next DXOA69C3", "Hoover H-Wash 500 HW411AMC", "Serie 6 WAU28PH9GB", "Serie 4 WAN28281GB","Serie 6 WAU28PH9GB", "WY940P44EB", "WMY1048LB1", "WMY1048LB1"]], 
            [[1,1,1,0,0,1,1,1,0,0],["Dryer"],"DRYER", ["Kitchen",],["TCFS83BGP", "NTM1182XBUK", "TCFS83BGP", "NTM1182XBUK", "TCFS83BGP", "Serie 4 WTR85V21GB", "Serie 6 WTWH7660GB", "Serie 4 WTR85V21GB", "IDCE8450BSH", "YTM1070KQFP"]], 
            [[1,1,1,1,1,1,1,1,2,0],["Microwave","Second Microwave"],"MICROWAVE", ["Kitchen","Kitchen"], ["NN-SD27HSBPQ", "NN-DF386BBPQ", "NN-CD87KSBPQ", "K25MMS14 Solo Microwave", "K30GMS18 Microwave with Grill", "K30CSS14 Combination Microwave","NN-SD27HSBPQ", "NN-DF386BBPQ", "NN-CD87KSBPQ", "K25MMS14 Solo Microwave"]], 
            [[2,2,2,2,2,1,1,0,0,1],["Livingroom TV","Bedroom TV"],"TV", ["Livingroom","Bedroom"], ["Samsung QE55Q80A", "Samsung UE50AU9000", "Samsung UE32T4300AKXXU", "Samsung QE55Q80A", "Samsung UE50AU9000", "Samsung UE32T4300AKXXU", "LG OLED65C1", "LG 55UP75006LF", "LG 43UP77006LB", "LG OLED65C1"]]]


solar_panels = ["Project Solar Evolution Elite 400", 400,
                "SunPower Maxeon 3", 385,
                "LG NeON H BiFacial", 440,
                "JA Solar JAM60S20", 380,
                "Panasonic HIT N 245W", 245,
                "Longi Hi-Mo 4m 445-465M", 455]
ids = []
consumption = [400, 200, 430, 385, 250, 370, 450, 270, 330, 400]
#objects = requests.get("http://127.0.0.1:8000/api/v1/getProducers/",).json()

address = []


 
mycsv = csv.reader(open('csv/fivethousaddr.csv'))
for row in mycsv:
   i = row[0].split(' ')
   address.append(i[1])
print(address)

'''
mycsv = csv.reader(open('csv/new_address.csv'))
for row in mycsv:
   address.append(row[0])
print(address[0])


for i in range(1, 1000):
    transactions = requests.post("http://127.0.0.1:8000/api/v1/createTransactions/",json={"id":i, "address":address[i-1]}).json()
'''
'''
for object in objects:
    ids.append(object['id'])

print(ids)
int = -1

for id in ids:
    int += 1
    data = {
        "name":"Solar Panel",
         "is_consuming_object":False,
         "type":"Solar_Panel",
         "room":"Roof",
         "reference":solar_panels[int%6],
         "owner":id,
         "consumption_per_minute":consumption[int%10],
    }
    object = requests.post("http://127.0.0.1:8000/api/v1/createObject/", json=data,)
'''
    

'''
address = []

mycsv = csv.reader(open('csv/new_address.csv'))
for row in mycsv:
   address.append(row[0])
print(address[0])
int = -1
pros = False
int = -1

mycsv = csv.reader(open('csv/thousand_names.csv'))
for row in mycsv:
      int +=1
      if int%3 == 0:
         pros = True
      else:
         pros = False
      print(row[0])
      data = {
         'password':'Unmotdepasse.1',
         'password2':'Unmotdepasse.1',
         'username':row[0],
         'email':row[0] + '@gmail.com',
         }
      data2 = {
         'name':row[0],
         'username':row[0],
         'address':address[int],
         'energy_mix_per_day':[[1,2,3],[3,2,1]],
         'overall_energy_mix':[1,2,3],
         'is_prosumer':pros,
         }
      user = requests.post("http://127.0.0.1:8000/api/v1/newUser/",json=data)
      object = requests.post("http://127.0.0.1:8000/api/v1/updateAccount2/", json=data2)
      print(object.json())
'''

'''
mycsv = csv.reader(open('csv/thousand_names.csv'))
for row in mycsv:
   for appliance in appliances:
      a_chance = random.randint(0,9)
      for i in range(appliance[0][a_chance]):
         a = random.randint(0,9)
         data = {"name":appliance[1][i],
                 "is_consuming_object":True,
                 "type":appliance[2],
                 "room":appliance[3][i],
                 "reference":appliance[4][a],
                 "owner":row[0],
                 "consumption_per_minute": random.randint(100,400)
       }
         requests.post("http://127.0.0.1:8000/api/v1/createObject/", json=data)


'''
   

'''

address = []

mycsv = csv.reader(open('new_address.csv'))
for row in mycsv:
   address.append(row[0])
print(address[0])
'''
"""
mycsv = csv.reader(open('thousand_names.csv'))
int = -1
pros = False
for row in mycsv:
   int +=1
   if int%3 == 0:
      pros = True
   else:
      pros = False
   print(row[0])
   data = {
        'name':row[0],
        'username':row[0],
        'email':row[0] + '@gmail.com',
        'address':address[int],
        'energy_mix_per_day':[[1,2,3],[3,2,1]],
        'overall_energy_mix':[1,2,3],
        'is_prosumer':pros,
        }

   object = requests.post("http://127.0.0.1:8000/api/v1/createTest/", json=data)
   print(object.json())
"""


