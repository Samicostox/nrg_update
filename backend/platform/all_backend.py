import time
import requests


# What should happen:
# At all time, transfer from consumers to prosumers should happen, transfer/ endpoint runing all the time,
# every minute all new transactions are added to the database for quick access, addTransactions/
# Every 5 seconds the amount of energy consumed and produced by users should be updated, it takes 4 seconds for the backend to do it, thus energyUpdate/ called at all time
# Every time the user consumes/produces energy the amount should be updated(Every day/hour?),
# Every minute all the processed transactions should be stored in the database to allow quick access.
# Every day the amount of energy consumed and produced plus the expenses or revenue of the day should be stored in the designated field.

'''
while(True):
    print("Main Process")
    st = time.time()
    
    res = requests.get("http://127.0.0.1:8000/api/v1/transferEnergy/").json()
    requests.get("http://127.0.0.1:8000/api/v1/updateEnergy/",)
    if(time.time()==st+60):
        requests.get("http://127.0.0.1:8000/api/v1/storeTransactions/").json()
'''
'''
while(True):
    print("Algorithm Comparaison")

    num_cons = [75,350,700,1500,3000]
    num_pros = [25,150,300,500,1000]
    
    for i in range(5):
        st = time.time()
        res = requests.post("http://127.0.0.1:8000/api/v1/transferEnergy2/", data={"num_pros":num_pros[i], "num_cons":num_cons[i]}).json()
        end = time.time()
        print("It took my method ", end-st, "secs to transfer ", res['Response'], " and match ", num_pros[i] + num_cons[i])
        
        res3 = requests.post("http://127.0.0.1:8000/api/v1/stableMariage2/", data={"num_pros":num_pros[i], "num_cons":num_cons[i]}).json()
        end3 = time.time()
        print("It took stable mariage ", end3-end, "secs to transfer ", res3['Response'], " and match ", num_pros[i] + num_cons[i])
        
        res2 = requests.post("http://127.0.0.1:8000/api/v1/new_gurobi2/", data={"num_pros":num_pros[i], "num_cons":num_cons[i]}).json()
        end2 = time.time()
        print("It took gurobi ", end2-end3, "secs to transfer ", res2['total'], " and match ", num_pros[i] + num_cons[i])
        
    
    time.sleep(5)
'''
while(True):
    print("Algorithm Comparaison")
    
    st = time.time()
    res = requests.get("http://127.0.0.1:8000/api/v1/transferEnergy/").json()
    end = time.time()
    print("It took my method ", end-st, "secs to transfer ", res['Response'])
    
    '''
    res3 = requests.get("http://127.0.0.1:8000/api/v1/stableMariage/").json()
    end3 = time.time()
    print("It took stable mariage ", end3-end, "secs to transfer ", res3['Response'])
    
    res2 = requests.get("http://127.0.0.1:8000/api/v1/new_gurobi/").json()
    end2 = time.time()
    print("It took gurobi ", end2-end3, "secs to transfer ", res2['total'])
    '''
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

