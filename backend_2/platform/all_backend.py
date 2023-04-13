import time
import requests


# What should happen:
# At all time, transfer from consumers to prosumers should happen, transfer/ endpoint runing all the time,
# every minute all new transactions are added to the database for quick access, addTransactions/
# Every 5 seconds the amount of energy consumed and produced by users should be updated, it takes 4 seconds for the backend to do it, thus energyUpdate/ called at all time
# Every time the user consumes/produces energy the amount should be updated(Every day/hour?),
# Every minute all the processed transactions should be stored in the database to allow quick access.
# Every day the amount of energy consumed and produced plus the expenses or revenue of the day should be stored in the designated field.


while(True):
    print("Main Process")
    st = time.time()
    res = requests.get("http://127.0.0.1:8000/api/v1/transferEnergy/").json()
    end = time.time()
    res2 = requests.get("http://127.0.0.1:8000/api/v1/gurobi/").json()
    end2 = time.time()
    res3 = requests.get("http://127.0.0.1:8000/api/v1/stableMariage/").json()
    end3 = time.time()
    
    print("It took my method ", end-st, "secs to transfer ", res['Response'])
    print("It took gurobi ", end2-end, "secs to transfer ", res2['Response'])
    print("It took stable mariage ", end3-end2, "secs to transfer ", res3['Response'])
    time.sleep(5)

while(True):
    print("Store transactions")
    requests.get("http://127.0.0.1:8000/api/v1/storeTransactions/").json()
    # should store all the new transactions every minute to make it faster for the front end to display all transactions
    time.sleep(60)

while(True):
    print("Dayly updates of user data")
    requests.get("http://127.0.0.1:8000/api/v1/updateEnergy/")
    #should update the following fields of all objects: expense_per_day, energy_per_day once a day
    time.sleep(86400)

while(True):
    print("Energy update")
    requests.get("http://127.0.0.1:8000/api/v1/updateEnergy/",)

