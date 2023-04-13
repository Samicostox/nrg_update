from asyncio import sleep
import requests


while(True):
        
        print("Energy Process")
        update_energy = requests.post("http://127.0.0.1:8000/api/v1/updateEnergy/",)
        