from rest_framework.decorators import api_view
from rest_framework import generics
from main.models import *
from api.serializers import *
from rest_framework.response import Response
from web3 import Web3
import os
import json
from datetime import datetime, timedelta
import pulp
import gurobipy as gp

# Create your views here.
class ListAccounts(generics.ListCreateAPIView):
  queryset = models.Account.objects.all()
  serializer_class = AccountSerializer



@api_view(['POST'])
def updateAccount(request):
   data = request.data
   account = Account.objects.get(username=data['username'])
   new_data = {
               'address': data['address'],
               'private_key': data['private_key']}
   accountSerializer = AccountSerializer(account, data=new_data, partial=True)
   if accountSerializer.is_valid():
      accountSerializer.save()
      return Response(accountSerializer.data)
   return Response(accountSerializer.errors)

@api_view(['POST'])
def updateObject(request):
   data = request.data
   object = Object.objects.get(pk=data['id'])
   new_data = {
               'is_on': data['is_on'],
               #'energy_per_minute': data['energy_per_minute']
               }
   objectSerializer = ObjectSerializer(object, data=new_data, partial=True)
   if objectSerializer.is_valid():
      objectSerializer.save()
      return Response(objectSerializer.data)
   return Response(objectSerializer.errors)




# Front-End related ---------------------------------------------------

@api_view(['POST'])
def registration_view(request):
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			#token = Token.objects.get(user=account).key
			data['id'] = account.pk
		else:
			data = serializer.errors
		return Response(data)

@api_view(['POST'])
def registration(request):
   data = request.data
   if data['password1'] == data['password2']:
      account = Account.objects.create(
      password=data['password1'],
      username=data['username'],
      email = data['email'],
      is_prosumer = data['is_prosumer'],
      )
      transaction = Transactions.objects.create(
         address = data['address'],
         user = account
      )
      serializer = AccountSerializer(account, many = False)
      return Response(serializer.data,)
   return Response({"Response":"The two passwords are not matching."})

@api_view(['POST'])
def createAccount(request):
   data = request.data
   account = Account.objects.create(
      password=data['password'],
      username=data['username'],
      name=data['name'],
      email=data['email'],
      address=data['address'],
      is_prosumer=data['is_prosumer'],
      )
   transaction = Transactions.objects.create(
      address = data['address'],
      user = account
   )
   serializer = AccountSerializer(account, many=False)
   return Response(serializer.data)

@api_view(['POST'])
def login(request):
   data = request.data
   account = Account.objects.get(username=data['username'])
   if not account:
      return {"Response":"Incorrect Username"}
   if account.password == data['password']:
      return Response({"id": account.pk, "is_prosumer":account.is_prosumer, "Response":"Login Successfull"})
   return Response(json.dumps({"Response":"Incorrect Password!"}))

@api_view(['GET'])
def getAccounts(request):
  accounts = Account.objects.all()
  serializer = AccountSerializer(accounts, many = True)
  return Response(serializer.data)

@api_view(['POST'])
def getAccount(request):
   data = request.data
   account = Account.objects.get(pk=data['id'])
   print(account)
   serializer = AccountSerializer(account, many=False)
   return Response(serializer.data)

@api_view(['POST'])
def getWeeklyEnergyMix(request):
   data = request.data
   account = Account.objects.get(pk=data['id'])

   grid = 0
   solar = 0
   wind = 0
   mix = []
   for day in account.weekly_energy_mix:
      grid += day[0]
      solar += day[1]
      wind += day[2]

   mix.append(grid)
   mix.append(solar)
   mix.append(wind)
   return Response({"Weekly Energy Mix":mix})

@api_view(['POST'])
def getOverallEnergyMix(request):
   data = request.data
   account = Account.objects.get(pk=data['id'])
   return Response({"Overall Energy Mix": account.overall_energy_mix})

# New version -----------------------------------------------------------

class ListObjects(generics.ListCreateAPIView):
  queryset = models.Object.objects.all()
  serializer_class = ObjectSerializer

@api_view(['POST'])
def changeProfileDetails(request):
   data = request.data
   account = Account.objects.get(pk=data['id'])
   new_data = {"energy_mix_per_day": data['energy_mix_per_day']}
   accountSerializer = AccountSerializer(account, data=new_data, partial=True)
   if accountSerializer.is_valid():
      accountSerializer.save()
      return Response(accountSerializer.data)
   return Response(accountSerializer.errors)

@api_view(['POST'])
def createObject(request):
   data = request.data
   owner = Account.objects.get(pk=data['owner'])
   object = Object.objects.create(
      name = data['name'],
      is_consuming_object = data['is_consuming_object'],
      type = data['type'],
      energy_per_minute = data['consumption_per_minute'],
      room = data['room'],
      model_reference = data['reference'],
      owner = owner,
   )
   serializer = ObjectSerializer(object, many = False)
   return Response(serializer.data)

@api_view(['POST'])
def switchObjectState(request):
   data = request.data
   object = Object.objects.get(pk=data['id'])
   new_data = {'is_on': not object.is_on}
   objectSerializer = ObjectSerializer(object, data=new_data, partial=True)
   if objectSerializer.is_valid():
      objectSerializer.save()
      return Response(objectSerializer.data)
   return Response(objectSerializer.errors)

@api_view(['POST'])
def deleteObject(request):
   data = request.data
   object = Object.objects.get(pk=data['id'])
   object.delete()
   return Response({'message': 'Object was deleted successfully!'})

@api_view(['POST'])
def desactivateObject(request):
   data = request.data
   object = Object.objects.get(pk=data['id'])
   new_data = {'is_active':False}
   objectSerializer = ObjectSerializer(object, data=new_data, partial=True)
   if objectSerializer.is_valid():
      objectSerializer.save()
      return Response(objectSerializer.data)
   return Response(objectSerializer.errors)

@api_view(['POST'])
def getAccountObject(request):
   data = request.data
   account = Account.objects.get(pk=data['id'])
   objects = Object.objects.filter(owner=account).filter(is_active=True).filter(is_consuming_object=data['is_consuming_object'])
   serializer = ObjectSerializer(objects, many=True)
   return Response(serializer.data)

@api_view(['POST'])
def getObjectsData(request):
   data = request.data
   owner = Account.objects.get(pk=data['id'])
   objects = Object.objects.filter(owner=owner).filter(is_consuming_object=data['is_consuming_object'])
   objectData = []
   groups = []
   total = 0
   for object in objects:
      if object.type in groups:
         objectData[groups.index(object.type)] = (object.type, object.overall_energy + objectData[groups.index(object.type)][1])
      else:
         objectData.append((object.type, object.overall_energy))
         groups.append(object.type)
      total += object.overall_energy
   objectData.sort(key=lambda a: a[1], reverse=True )
   if len(objectData) > 3:
      other = 0
      for i in range (4, len(objectData)):
         other += objectData[i][1]
      objectData = objectData[:4]
      objectData.append(("Other", other))
   objectData.append(("Total",total))
   print(objectData)
   return Response({"Consumption":objectData})

@api_view(['POST'])
def getObjectsWeeklyData(request):
   data = request.data 
   owner = Account.objects.get(pk=data['id'])
   objects = Object.objects.filter(owner=owner).filter(is_consuming_object=data['is_consuming_object'])
   weeklyData = []
   groups = {}
   total = 0
   for object in objects:
      
      object.energy_per_day.reverse()
      if object.energy_per_day:
         if object.type in groups.keys():
            for j in range (min(14,len(object.energy_per_day))):
               groups[object.type][j] += object.energy_per_day[j]  
         else:
            if len(object.energy_per_day) < 14:
               groups[object.type] = object.energy_per_day
               for i in range (14-object.energy_per_day):
                  groups[object.type].append(0)
            else:
               groups[object.type] = object.energy_per_day[:14]
   print(groups)
   res = []
   days = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
   for g in groups.keys():
      res.append([g,groups[g]])
      a = 0
      for i in groups[g]:
         days[a] += i
         a+=1
   res.append(days)
   return Response({'res':res})




@api_view(['POST'])
def getObjectsWeeklyData2(request):
   data = request.data 
   owner = Account.objects.get(pk=data['id'])
   objects = Object.objects.filter(owner=owner).filter(is_consuming_object=data['is_consuming_object'])
   weeklyData = []
   groups = []
   total = 0
   for i in range(14):
    objectData = []
    total = 0
    for object in objects:
        leng = len(object.energy_per_day)
        print(leng - i - 1)
        print(len(object.energy_per_day))
        
        if leng - i < 0 or leng-i-1 < 0:
           break
        elif object.type in groups:
          print(groups)
          objectData[groups.index(object.type)] = (object.type, object.energy_per_day[leng - i-1] + objectData[groups.index(object.type)][1])
        else:
          objectData.append((object.type, object.energy_per_day[leng - i - 1]))
          groups.append(object.type)
        total += object.energy_per_day[leng - i-1]
    objectData.sort(key=lambda a: a[1], reverse=True)
    if len(objectData) > 3:
      other = 0
      for i in range (4, len(objectData)):
         other += objectData[i][1]
      objectData = objectData[:4]
      objectData.append(("Other", other))
    objectData.append(("Total",total))

    weeklyData.append(objectData)
   weeklyData.reverse()
   print(weeklyData)
   return Response({"Weekly Consumption":weeklyData})


@api_view(['POST'])
def getObjectsExpenses(request):
   data = request.data
   consumer = Account.objects.get(pk=data['id'])
   objects = Object.objects.filter(owner=consumer).filter(is_consuming_object=data['is_consuming_object'])
   objectData = []
   groups = []
   total = 0
   for object in objects:
      if object.type in groups:
         objectData[groups.index(object.type)] = (object.type, object.overall_expense + objectData[groups.index(object.type)][1])
      else:
         objectData.append((object.type, object.overall_expense))
         groups.append(object.type)
      total += object.overall_expense
   objectData.sort(key=lambda a: a[1], reverse=True )
   if len(objectData) > 3:
      other = 0
      for i in range (4, len(objectData)):
         other += objectData[i][1]
      objectData = objectData[:4]
      objectData.append(("Other", other))
   objectData.append(("Total",total))
   print(objectData)
   return Response({"Expense":objectData})

@api_view(['POST'])
def getObjectsWeeklyExpenses(request):
   data = request.data 
   owner = Account.objects.get(pk=data['id'])
   objects = Object.objects.filter(owner=owner).filter(is_consuming_object=data['is_consuming_object'])
   weeklyData = []
   groups = {}
   total = 0
   for object in objects:
      
      object.expense_per_day.reverse()
      if object.expense_per_day:
         if object.type in groups.keys():
            for j in range (min(14,len(object.expense_per_day))):
               groups[object.type][j] += object.expense_per_day[j]  
         else:
            if len(object.expense_per_day) < 14:
               groups[object.type] = object.expense_per_day
               for i in range (14-object.expense_per_day):
                  groups[object.type].append(0)
            else:
               groups[object.type] = object.expense_per_day[:14]
   print(groups)
   res = []
   days = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
   for g in groups.keys():
      res.append([g,groups[g]])
      a = 0
      for i in groups[g]:
         days[a] += i
         a+=1
   res.append(days)
   return Response({'res':res})

@api_view(['POST'])
def getObjectsWeeklyExpenses2(request):
   data = request.data 
   consumer = Account.objects.get(pk=data['id'])
   objects = Object.objects.filter(owner=consumer).filter(is_consuming_object=data['is_consuming_object'])
   weeklyData = []
   groups = []
   total = 0
   for i in range(14):
    objectData = []
    total = 0
    for object in objects:
        leng = len(object.expense_per_day)
        print(leng)
        print(objectData)
        
        if leng - i < 0:
           break
        elif object.type in groups:
          print(groups.index(object.type))
          objectData[groups.index(object.type)] = (object.type, object.expense_per_day[leng - i-1] + objectData[groups.index(object.type)][1])
        else:
          objectData.append((object.type, object.expense_per_day[leng - i - 1]))
          groups.append(object.type)
        total += object.expense_per_day[leng - i - 1  ]
    objectData.sort(key=lambda a: a[1], reverse=True)
    if len(objectData) > 3:
      other = 0
      for i in range (4, len(objectData)):
         other += objectData[i][1]
      objectData = objectData[:4]
      objectData.append(("Other", other))
    objectData.append(("Total",total))

    weeklyData.append(objectData)
   weeklyData.reverse()
   print(weeklyData)
   return Response({"Weekly Expense":weeklyData})

# Token related -------------------------------------------------------------

@api_view(['GET'])
def getBalanceOf(request, username):
  user = Account.objects.get(username=username)
  w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
  contractAddress = Contract.objects.get(name='NRGToken').address
  with open('api/assets/NRGToken.json', 'r') as file:
      nrgJson = json.load(file)
  abi = nrgJson["abi"]
  nonce = w3.eth.getTransactionCount(user.address)
  nrg_token = w3.eth.contract(address=contractAddress, abi=abi)
  
  response = {"Balance": nrg_token.functions.getBalance(user.address).call()}
  return Response(json.dumps(response))

@api_view(['GET'])
def getBalanceOfTest(request):
  data = request.data
  username = data['username']
  user = Account.objects.get(username=username)
  w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
  contractAddress = Contract.objects.get(name='NRGToken').address
  with open('api/assets/NRGToken.json', 'r') as file:
      nrgJson = json.load(file)
  abi = nrgJson["abi"]
  nonce = w3.eth.getTransactionCount(user.address)
  nrg_token = w3.eth.contract(address=contractAddress, abi=abi)
  
  response = {"Balance": nrg_token.functions.getBalance(user.address).call()}
  return Response(json.dumps(response))

@api_view(['GET'])
def deploy_contract(request):
  contract = Contract.objects.get(name='NRGToken')
  contract.delete()
  with open('api/assets/NRGToken2.json', 'r') as file:
      nrgJson = json.load(file)

  abi = nrgJson["abi"]
  bytecode = nrgJson["bytecode"]

  w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
  chain_id = 1337
  my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
  #private_key = os.getenv("PRIVATE_KEY")
  private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"

  NRGToken = w3.eth.contract(abi=abi, bytecode=bytecode)
  # Get the latest transaction
  nonce = w3.eth.getTransactionCount(my_address)

  # Build a transaction
  # Sign a transaction
  # Send a transaction
  transaction = NRGToken.constructor().buildTransaction({"chainId":chain_id, "from":my_address, "nonce":nonce})
  signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

  tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
  tx_receip = w3.eth.wait_for_transaction_receipt(tx_hash)
  contract = Contract.objects.create(
      name='NRGToken',
      address= tx_receip.contractAddress,
      )
  serializer = ContractSerializer(contract, many=False)
  return Response(serializer.data)
 

@api_view(['POST'])
def transfer(request):
  data = request.data
  _to = data["to"]
  _amount = data["amount"]
  w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
  with open('api/assets/NRGToken.json', 'r') as file:
      nrgJson = json.load(file)
  abi = nrgJson["abi"]
  chain_id = 1337
  my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
  private_key = os.getenv("PRIVATE_KEY")
  contractAddress = Contract.objects.get(name='NRGToken').address

  nonce = w3.eth.getTransactionCount(my_address)
  nrg_token = w3.eth.contract(address=contractAddress, abi=abi)
  
  store_transaction = nrg_token.functions.transfer(_to, int(_amount)).buildTransaction(
  {"chainId": chain_id, "from":my_address, "nonce":nonce}
  )
  nonce +=1
  signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
  send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
  tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
  print(nrg_token.functions.getBalance(my_address).call())

  return Response({'Response': 'Success'})


@api_view(['POST'])
def mint(request):
  data = request.data
  _to = data["_to"]
  _amount = data["_amount"]
  w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
  with open('api/assets/NRGToken2.json', 'r') as file:
    nrgJson = json.load(file)
  abi = nrgJson["abi"]
  chain_id = 1337
  my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
  private_key = os.getenv("PRIVATE_KEY")
  contractAddress = Contract.objects.get(name='NRGToken').address
  nonce = w3.eth.getTransactionCount(my_address)
  nrg_token = w3.eth.contract(address=contractAddress, abi=abi)
  store_transaction = nrg_token.functions.mint(_to, int(_amount)).buildTransaction(
    {"chainId": chain_id, "from":my_address, "nonce":nonce, "gasPrice":100}
  )
  nonce += 1
  signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
  send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
  tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
  print(nrg_token.functions.getBalance(_to).call())

  return Response({'Response': 'Success'})

@api_view(['POST'])
def burn(request):
  data = request.data
  _to = data["_to"]
  _amount = data["_amount"]
  w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
  with open('api/assets/NRGToken.json', 'r') as file:
    nrgJson = json.load(file)
  abi = nrgJson["abi"]
  chain_id = 1337
  my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
  private_key = os.getenv("PRIVATE_KEY")
  contractAddress = Contract.objects.get(name='NRGToken').address
  nonce = w3.eth.getTransactionCount(my_address)
  nrg_token = w3.eth.contract(address=contractAddress, abi=abi)
  store_transaction = nrg_token.functions.burn(_to, int(_amount)).buildTransaction(
    {"chainId": chain_id, "from":my_address, "nonce":nonce, "gasPrice":606581616}
  )
  nonce += 1
  signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
  send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
  tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
  print(nrg_token.functions.getBalance(_to).call())

  return Response({'Response': 'Success'})

@api_view(['POST'])
def transferFrom(request):
  data = request.data
  _from = data["from"]
  _to = data["to"]
  _amount = data["amount"]
  w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
  with open('api/assets/NRGToken.json', 'r') as file:
      nrgJson = json.load(file)
  abi = nrgJson["abi"]
  chain_id = 1337
  my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
  private_key = os.getenv("PRIVATE_KEY")
  contractAddress = Contract.objects.get(name='NRGToken').address

  nonce = w3.eth.getTransactionCount(my_address)
  nrg_token = w3.eth.contract(address=contractAddress, abi=abi)
  
  
  '''
  store_transaction = nrg_token.functions.transferFrom(_from, _to, int(_amount)).buildTransaction(
  {"chainId": chain_id, "from":my_address, "nonce":nonce, "gas":210000}
  )
  '''
  store_transaction = w3.eth.send_transaction({
  'to': _to,
  'from': _from,
  'value': 12345,
  'gas': 21000,
  'maxFeePerGas': w3.toWei(250, 'gwei'),
  'maxPriorityFeePerGas': w3.toWei(2, 'gwei'),
})
  #print(store_transaction)
  nonce +=1
  #signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
  #send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
  tx_receipt = w3.eth.wait_for_transaction_receipt(store_transaction)
  #print(tx_receipt)
  #print(w3.eth.getBlock(165))
  #print(w3.eth.get_balance(_from, block_identifier=218))

  return Response({'Response': 'Success'})

# Trading platform related -------------------------------------------------

@api_view(['PUT'])
def modifyConsumption(request):
  data = request.data
  user = Account.objects.get(name=data['username'])
  new_data = {'consuming': data['consuming']}
  accountSerializer = AccountSerializer(user, data=new_data, partial=True)
  if accountSerializer.is_valid():
      accountSerializer.save()
      return Response(accountSerializer.data)
  return Response(accountSerializer.errors)
  
@api_view(['PUT'])
def modifyProduction(request):
  data = request.data
  user = Account.objects.get(name=data['username'])
  new_data = {'producing': data['producing']}
  accountSerializer = AccountSerializer(user, data=new_data, partial=True)
  if accountSerializer.is_valid():
      accountSerializer.save()
      return Response(accountSerializer.data)
  return Response(accountSerializer.errors)

@api_view(['GET'])
def getConsumingUsers(request):
  now = datetime.now()
  consumers = Account.objects.filter(is_prosumer=False)
  users = consumers.filter(last_consumption__gt=now - timedelta(days=1))
  serializer = AccountSerializer(consumers, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def getProducingUsers(request):
  now = datetime.now()
  producers = Account.objects.filter(is_prosumer=True)
  users = producers.filter(last_production__gt=now - timedelta(days=1))
  serializer = AccountSerializer(producers, many=True)
  return Response(serializer.data)

@api_view(['PUT'])
def updateSurplus(request):
  data = request.data
  prosumer = Account.objects.get(username=data['username'])
  new_data = {'surplus': prosumer.producing - prosumer.consuming}
  accountSerializer = AccountSerializer(prosumer, data=new_data, partial=True)
  if accountSerializer.is_valid():
      accountSerializer.save()
      return Response(accountSerializer.data)
  return Response(accountSerializer.errors)

@api_view(['GET'])
def getProducers(request):
  producers = Account.objects.filter(is_prosumer=True)
  serializer = TransferSerializer(producers, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def getConsumers(request):
  consumers = Account.objects.filter(is_prosumer=False)
  serializer = TransferSerializer(consumers, many=True)
  return Response(serializer.data)

@api_view(['POST'])
def getObjects(request):
  data = request.data
  objects = Object.objects.filter(is_prosumer=data['is_prosumer'])
  serializer = ObjectSerializer(objects, many=True)
  return Response(serializer.data)

  
@api_view(['GET'])
def updateEnergy(request):
   consumers = Account.objects.all()
   ids = []
   for consumer in consumers:
      consuming = 0
      producing = 0
      objects = Object.objects.filter(owner=consumer)
      for object in objects:
         if object.is_on and object.is_consuming_object:
            consuming += object.energy_per_minute
            object.todays_energy =+ object.energy_per_minute
         elif object.is_on and not object.is_consuming_object:
            producing += object.energy_per_minute
            object.todays_energy =+ object.energy_per_minute
         object.save()
         
      new_data = {'consuming': consuming, 'producing': producing}
      accountSerializer = AccountSerializer(consumer, data=new_data, partial=True)
      if accountSerializer.is_valid():
            accountSerializer.save()
   return Response({"Response": "Users energy has been updated!"})

@api_view(['GET'])
def transferEnergy(request):
   consumers = list(Account.objects.filter(is_prosumer=False))
   producers = list(Account.objects.filter(is_prosumer=True))
   w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
   a = 0
   bundle = []
   while producers and consumers:
                
         consumer = consumers[0]
         producer = producers[0]
         amount = min(consumer.consuming, producer.producing)
         store_transaction = w3.eth.send_transaction({
         'to': producer.address,
         'from': consumer.address,
         'value': amount,
         'gas': 21000,
         'maxFeePerGas': w3.toWei(250, 'gwei'),
         'maxPriorityFeePerGas': w3.toWei(2, 'gwei'),
         })
         a += amount

         consumer.consuming -= amount
         producer.producing -= amount
         if not producer.producing:
            del producers[0]
         if not consumer.consuming:
            del consumers[0]

   print(a)
   return Response({"Response":a})

@api_view(['GET'])
def betterTransferEnergy(request):
   consumers = list(Account.objects.filter(is_prosumer=False))
   producers = list(Account.objects.filter(is_prosumer=True))
   w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
   a = -1
   bundle = []
   while producers and consumers:
         a += 1
         
         consumer = consumers[0]
         producer = producers[0]
         amount = min(consumer.consuming, producer.producing)
         store_transaction = w3.eth.send_transaction({
         'to': producer.address,
         'from': consumer.address,
         'value': amount,
         'gas': 21000,
         'maxFeePerGas': w3.toWei(250, 'gwei'),
         'maxPriorityFeePerGas': w3.toWei(2, 'gwei'),
         })
         consumer.consuming -= amount
         producer.producing -= amount
         if not producer.producing:
            del producers[0]
         if not consumer.consuming:
            del consumers[0]
         else:
            consumers.append(consumer)
            del consumers[0]
         if a % 5:
            tx_hash = w3.eth.sen
   print(a)
   return Response({"Response":a})

@api_view(['GET'])
def stableMariage(request):
   w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
   matching = {}
   consumers = [(x.address,x.consuming) for x in list(Account.objects.filter(is_prosumer=False))]
   producers = [(x.address,x.consuming) for x in list(Account.objects.filter(is_prosumer=True))]
   consumers = sorted(consumers, key=lambda d: d[1])
   producers = sorted(producers, key=lambda d: d[1])
   a = 0
   while consumers:
      a+=1
      consumer = consumers.pop(0)
      for producer in producers:
         if (producer) not in matching or (matching[(producer)][1] < consumer[1] and producer[1] > consumer[1]):
             # Update the matching
             if (producer) in matching:
                 consumers.append(matching[(producer)])
             matching[(producer)] = (consumer)
             break
         
   total = 0
   for match in matching:
      amount = min(match[1], matching[match][1])
      store_transaction = w3.eth.send_transaction({
         'to': match[0],
         'from': matching[match][0],
         'value': amount,
         'gas': 21000,
         'maxFeePerGas': w3.toWei(250, 'gwei'),
         'maxPriorityFeePerGas': w3.toWei(2, 'gwei'),
         })
      total += int(matching[match][1])

   #print(total)
   #print(matching)
   #print(len(matching))
   return Response({"Response":total})
                
@api_view(['GET'])
def stableMariageBetter(request):
   matching = {}
   consumers = [(x.address,x.consuming) for x in list(Account.objects.filter(is_prosumer=False))]
   producers = [(x.address,x.consuming) for x in list(Account.objects.filter(is_prosumer=True))]
   consumers = sorted(consumers, key=lambda d: d[1])
   producers = sorted(producers, key=lambda d: d[1])
   a = 0
   while producers:
      a+=1
      print(a)
      producer = producers.pop(0)
      for consumer in consumers:
         if (consumer) not in matching or matching[(consumer)][1] < producer[1]:
             # Update the matching
             if (consumer) in matching:
                 producers.append(matching[(consumer)])
             matching[(consumer)] = (producer)
             break
   print(matching)
   return Response({"Reponse":"ok"})

@api_view(['GET'])
def linearSolution(request):
    consumers = [(x.address,x.consuming) for x in list(Account.objects.filter(is_prosumer=False))]
    producers = [(x.address,x.consuming) for x in list(Account.objects.filter(is_prosumer=True))]
    consumers = sorted(consumers, key=lambda d: d[1])
    producers = sorted(producers, key=lambda d: d[1])

    consumers_indices = {buyer[0]: i for i, buyer in enumerate(consumers)}
    producers_indices = {seller[0]: i for i, seller in enumerate(producers)}

    n_consumers = len(consumers)
    n_producers = len(producers)
    M = [[0] * n_producers for i in range(n_consumers)]

    # Set up the linear programming problem
    prob = pulp.LpProblem("Matching problem", pulp.LpMaximize)
    obj = []
    constraints = []

    # Define the decision variables
    for i in range(n_consumers):
        for j in range(n_producers):
            x = pulp.LpVariable(f"x_{i}_{j}", lowBound=0)
            obj.append(x * producers[j][1])
            constraints.append(x <= consumers[i][1])
            constraints.append(x <= producers[j][1])
            M[i][j] = x

    # Define the objective function
    prob += pulp.lpSum(obj)

    # Add the constraints
    for c in constraints:
        prob += c

    # Solve the linear programming problem
    prob.solve()

    # Get the optimal matching
    M_star = [[M[i][j].varValue for j in range(n_producers)] for i in range(n_consumers)]

    matching = {}
    for i, consumer in enumerate(consumers):
        for j, producer in enumerate(producers):
            if M_star[i][j] > 0:
                matching[consumer[0]] = (producer[0], M_star[i][j])
                break

    print(matching)
    return Response({"Response": "OK"})

@api_view(['GET'])
def gurobi(request):
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    consumers = [(x.address,x.consuming) for x in list(Account.objects.filter(is_prosumer=False))]
    producers = [(x.address,x.consuming) for x in list(Account.objects.filter(is_prosumer=True))]
    buyers = sorted(consumers, key=lambda d: d[1])
    sellers = sorted(producers, key=lambda d: d[1])
   # Create dictionaries to map buyer and seller names to indices
    buyer_indices = {buyer[0]: i for i, buyer in enumerate(buyers)}
    seller_indices = {seller[0]: i for i, seller in enumerate(sellers)}

    # Initialize the model
    model = gp.Model()

    # Define the decision variables
    n_buyers = len(buyers)
    n_sellers = len(sellers)
    x = model.addVars(n_buyers, n_sellers, lb=0)

    # Define the objective function
    obj = gp.quicksum(min(sellers[j][1], buyers[j][1]) * x[i, j] for i in range(n_buyers) for j in range(n_sellers))
    model.setObjective(obj, gp.GRB.MAXIMIZE)

    # Add the constraints
    for i in range(n_buyers):
        model.addConstr(gp.quicksum(x[i, j] for j in range(n_sellers)) <= buyers[i][1])
    for j in range(n_sellers):
        model.addConstr(gp.quicksum(x[i, j] for i in range(n_buyers)) <= sellers[j][1])

    # Optimize the model
    model.optimize()

    # Get the optimal matching
    M_star = [[x[i, j].x for j in range(n_sellers)] for i in range(n_buyers)]

    # Convert the matrix M* to a dictionary of matches
    matching = {}
    total = 0
    for i, buyer in enumerate(buyers):
        for j, seller in enumerate(sellers):
            if M_star[i][j] > 0:
                matching[buyer[0]] = (seller[0], M_star[i][j])
                break 
    for match in matching:

      store_transaction = w3.eth.send_transaction({
         'to': match,
         'from': matching[match][0],
         'value': int(matching[match][1]),
         'gas': 21000,
         'maxFeePerGas': w3.toWei(250, 'gwei'),
         'maxPriorityFeePerGas': w3.toWei(2, 'gwei'),
         })
      total += int(matching[match][1])

    print(total)
    #print(len(matching))
    return Response({"Response":total})

@api_view(['GET'])
def storeTransactions(request):
   w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
   
   transactions = Transactions.objects.all()
   latest_block = w3.eth.blockNumber
   for transaction in transactions:
      user_transactions = []
      address = transaction.address
      last = transaction.last_block

      for block_number in range(last, latest_block + 1):
      # Get the block at the current block number
         block = w3.eth.getBlock(block_number, True)

         # Loop through all the transactions in the block
         for tx in block.transactions:
            # Check if the user is the sender or receiver of the transaction
            if tx['from'] == address or tx['to'] == address:
                  if transaction.transactions:
                     transaction.transactions.append((tx['from'], tx['to'], tx['value']))
                     transaction.save()
                  elif not transaction.transactions:
                     transaction.transactions = [(tx['from'], tx['to'], tx['value'])]
                     transaction.save()

      transaction.last_block = block_number
      transaction.save()

@api_view(['POST'])
def addTransactions(request):
   data = request.data
   w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

   user = Account.objects.get(id=data['id'])
   transactions = Transactions.objects.get(user=user)
   user_address = user.address

   # Get the latest block number
   latest_block = w3.eth.blockNumber

   # List to store the user's transactions
   user_transactions = []


   # Loop through all the blocks to find transactions involving the user
   for block_number in range(latest_block + 1):
      # Get the block at the current block number
      block = w3.eth.getBlock(block_number, True)

      # Loop through all the transactions in the block
      for tx in block.transactions:
         # Check if the user is the sender or receiver of the transaction
         if tx['from'] == user_address or tx['to'] == user_address:
               print(tx)
               transactions.transactions = transactions.transactions.append((tx['from'], tx['to'], tx['value']))
               user_transactions.append(tx)
               transactions.save()

   # Print the list of user transactions
   print(user_transactions)
   return Response({"Response":"Transactions successfully updated"})

@api_view(['POST'])
def createTransactions(request):
   data = request.data
   user = Account.objects.get(id=data['id'])
   transaction = Transactions.objects.create(
      user = user,
      address=data['address']
   )
   serializer = TransactionsSerializer(transaction, many=False)
   return Response(serializer.data)

@api_view(['POST'])
def getTransactions(request):
   data = request.data
   #user = Account.objects.get(address=data['id'])
   res = []
   transactions = Transactions.objects.filter(address=data['id'])
   serializer = TransactionsSerializer(transactions, many=True)
   for transaction in transactions:
      res.append(transaction.transactions)
   return Response({"transactions":res[0  ]})

@api_view(['GET'])
def dailyDataUpdate(request):
   objects = Object.objects.all()
   for object in objects:
      object.energy_per_day = object.energy_per_day.append(object.todays_energy)
      object.expense_per_day = object.expense_per_day.append(object.todays_expense)
   return Response({"Response": "All updates done successfully"})

@api_view(['DELETE'])
def deleteAllTransactions(request):
   transactions = Transactions.objects.all()
   transactions.delete()
   return Response({"Res":"ok"})


@api_view(['GET'])
def modifyObjects(request):
   objects = Object.objects.all()
   a = 0
   print("ok")
   energy = [6.1, 1.4, 2.2, 3.4, 4.3, 5, 4.7]
   for object in objects:
      a += 1
      for i in range(365):
         if len(object.energy_per_day):
            object.energy_per_day.append(energy[(i+a)%7]*object.energy_per_minute)
            object.overall_energy += energy[(i+a)%7]*object.energy_per_minute
            object.expense_per_day.append(energy[(i+a)%7]*object.energy_per_minute*0.00034)
            object.overall_expense += energy[(i+a)%7]*object.energy_per_minute*0.00034
            
            
         else:
            object.energy_per_day = [energy[(i+a)%7]*object.energy_per_minute]
            object.overall_energy += energy[(i+a)%7]*object.energy_per_minute
            object.expense_per_day = [energy[(i+a)%7]*object.energy_per_minute*0.00034]
            object.overall_expense += energy[(i+a)%7]*object.energy_per_minute*0.00034
         object.save()
   return Response({"res":"ok"})
