from django.urls import path
from . import views
from api.views import *

urlpatterns = [
    
  path('', views.getRoutes, name='getRoutes'),

  path('add4000/', views.add4000, name='add4000'),
  path('electricityPrices/', views.getElectricityPrices, name='getElectricityPrices'),
  path('nrgPrices/', views.getNRGPrices, name='getNRGPrices'),

  path('max/', views.max, name='max'),
  path('max2/', views.max2, name='max2'),
  path('galeShapley/', views.gale_shapley, name='galeShapley'),
  path('new_gurobi/', views.new_gurobi, name='new_gurobi'),
  path('new_stable/', views.stableMariageBetter, name='stableMariageBetter'),

  path('transferEnergy2/', views.transferEnergy2, name='transferEnergy2'),
  path('stableMariage2/', views.stableMariage2, name='stableMariage2'),
  path('new_gurobi2/', views.new_gurobi2, name='new_gurobi2'),

  path('account/', ListAccounts.as_view(), name='ListAccounts'),
  path('objects/', ListObjects.as_view(), name='ListObjects'),
  path('modifyObject/', views.modifyObjects, name='modifyObjects'),

    # Account/Registration
  path('changeProfileDetails/', views.changeProfileDetails, name='changeProfileDetails'),
  path('createAccount/', views.createAccount, name='createAccount'),
  path('updateAccount/', views.updateAccount, name='updateAccount'),
  path('register/', views.registration, name='register'),
  path('login/', views.login, name="login"),
  path('newUser/', views.registration_view, name='registration_view'),
  path('updateAccount2/', views.updateAccount2, name='updateAccount2'),
  path('deleteAccount/', views.deleteAccount, name='deleteAccount'),

    # Objects
  path('updateObject/', views.updateObject, name='updateObject'),
  path('getAccountObject/', views.getAccountObject, name='getAccountObject'),
  path('switchObjectState/', views.switchObjectState, name='switchObjectState'),
  path('deleteObject/', views.deleteObject, name='deleteObject'),
  path('desactivateObject/', views.desactivateObject, name='desactivateObject'),
  path('createObject/', views.createObject, name='createObject'),
  path('switch/', views.switchOn, name='switchOn'),
  path('getAccountObjects/', views.getAccountObjects, name='getAccountObjects'),

    # Energy/Expenses/Data
  path('updateEnergy/', views.updateEnergy, name='updateEnergy'),
  path('objectData/', views.getObjectsData, name='getObjectsData'),
  path('weeklyObjectData/', views.getObjectsWeeklyData, name='getObjectsWeeklyData'),
  path('objectExpenses/', views.getObjectsExpenses, name='getObjectsExpenses'),
  path('weeklyObjectExpenses/', views.getObjectsWeeklyExpenses, name='getObjectsWeeklyExpenses'),
  path('weeklyEnergyMix/', views.getWeeklyEnergyMix, name='getWeeklyEnergyMix'),
  path('overallEnergyMix/', views.getOverallEnergyMix, name='getOverallEnergyMix'),
  path('dailyDataUpdates/', views.dailyDataUpdate, name='dailyDataUpdate'),
  # Blockchain
  # Blockchain
  path('transferEnergy/', views.transferEnergy, name='transferEnergy'),
  path('stableMariage/', views.stableMariage, name='stableMariage'),
  path('linearSolution/', views.linearSolution, name='linearSolution'),
  path('gurobi/', views.gurobi, name='gurobi'),

  path('getTransactions/', views.getTransactions, name='getTransactions'),
  path('createTransactions/', views.createTransactions, name='createTransactions'),
  path('addTransactions/', views.addTransactions, name='addTransactions'),
  path('storeTransactions/', views.storeTransactions, name='storeTransactions'),
  path('deleteAllTransactions/', views.deleteAllTransactions, name='deleteAllTransactions'),

  path('getBalanceOf/<str:username>/', views.getBalanceOf, name='getBalanceOf'),
  path('deployContract/', views.deploy_contract, name='deployContract'),
  path('transfer/', views.transfer, name='transfer'),
  path('transferFrom/', views.transferFrom, name='transferFrom'),

  # Test
  path('getBalanceOfTest/', views.getBalanceOfTest, name='getBalanceOfTest'),

  # Not in use (To be checked)
  path('currConsuming/', views.getConsumingUsers, name='getConsumingUsers'),
  path('currProducing/', views.getProducingUsers, name='getProducingUsers'),

  path('accounts/', views.getAccounts, name='getAccounts'),
  path('account/', views.getAccount, name='getAccount'),

  path('modifyConsumption/', views.modifyConsumption, name='modifyConsumption'),
  path('modifyProduction/', views.modifyProduction, name='modifyProduction'),

  # path('updateEnergy/', views.updateEnergy, name='updateEnergy'),  # This path is duplicated, so it's commented out.
  path('getProducers/', views.getProducers, name='getProducers'),
  path('getConsumers/', views.getConsumers, name='getConsumers'),
  path('getObjects/', views.getObjects, name='getObjects'),
]