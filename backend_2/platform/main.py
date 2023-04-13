import time
import requests


while(True):
          print("Main Process")
          consumers = requests.get("http://127.0.0.1:8000/api/v1/getConsumers/").json()
          producers = requests.get("http://127.0.0.1:8000/api/v1/currProducing").json()
                
          consumers = sorted(consumers, key=lambda d: d['consuming'])
          producers = sorted(producers, key=lambda d: d['producing'])
          a = 0
          st = time.time()
          while producers and consumers:
                
                consumer = consumers[0]
                producer = producers[0]
                #print("User: ", producer['username'], " is producing ", producer['producing'])
                #print("User: ", consumer['username'], " is consuming ", producer['consuming'])
                a += 1
                #print(a)
                amount = min(consumer['consuming'], producer['producing'])
                data = {'from': producer['address'],
                        'to': consumer['address'],
                        'amount': amount}
                #print(data)
                transaction = requests.post(url = "http://127.0.0.1:8000/api/v1/transferFrom/", data=data)
                #print(transaction.json())
                #print(data)
                        
                consumer['consuming'] -= amount
                producer['producing'] -= amount
                if not producer['producing']:
                    del producers[0]
                if not consumer['consuming']:
                    del consumers[0]
                else:
                    consumers.append(consumer)
                    del consumers[0]
          end = time.time()
          print("Done in", end - st, "sec")
          time.sleep(5)