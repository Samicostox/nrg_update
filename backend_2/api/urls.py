from django.urls import path
from . import views
from api.views import *

urlpatterns = [
  path('account/', ListAccounts.as_view()),
  path('objects/', ListObjects.as_view()), 
  path('modifyObject/', views.modifyObjects),


  # Account/Registration
  path('changeProfileDetails/', views.changeProfileDetails),
  path('createAccount/', views.createAccount),
  path('updateAccount/', views.updateAccount),
  path('register/', views.registration),
  path('login/', views.login),

  # Objects
  path('updateObject/', views.updateObject),
  path('getAccountObject/', views.getAccountObject),
  path('switchObjectState/', views.switchObjectState),
  path('deleteObject/', views.deleteObject),
  path('desactivateObject/', views.desactivateObject),
  path('createObject/', views.createObject),

  # Energy/Expenses/Data
  path('updateEnergy/', views.updateEnergy),
  path('objectData/', views.getObjectsData),
  path('weeklyObjectData/', views.getObjectsWeeklyData),
  path('objectExpenses/', views.getObjectsExpenses),
  path('weeklyObjectExpenses/', views.getObjectsWeeklyExpenses),
  path('weeklyEnergyMix/', views.getWeeklyEnergyMix),
  path('overallEnergyMix/', views.getOverallEnergyMix),
  path('dailyDataUpdates/', views.dailyDataUpdate),

  # Blockchain
  path('transferEnergy/', views.transferEnergy),
  path('stableMariage/', views.stableMariage),
  path('linearSolution/', views.linearSolution),
  path('gurobi/', views.gurobi),

  path('getTransactions/', views.getTransactions),
  path('createTransactions/', views.createTransactions),
  path('addTransactions/', views.addTransactions),
  path('storeTransactions/', views.storeTransactions),
  path('deleteAllTransactions/', views.deleteAllTransactions),

  path('getBalanceOf/<str:username>/', views.getBalanceOf),
  path('deployContract/', views.deploy_contract),
  path('transfer/', views.transfer),
  path('transferFrom/', views.transferFrom),
  path('mint/', views.mint),
  path('burn/', views.burn),

  # Test
  path('getBalanceOfTest/', views.getBalanceOfTest),

  # Not in use (To be checked)
  
  path('currConsuming/', views.getConsumingUsers),
  path('currProducing/', views.getProducingUsers),
  

  path('accounts/', views.getAccounts),
  path('account/', views.getAccount),


  path('modifyConsumption/', views.modifyConsumption),
  path('modifyProduction/', views.modifyProduction),

  #path('updateEnergy/', views.updateEnergy),
  path('getProducers/', views.getProducers),
  path('getConsumers/', views.getConsumers),
  path('getObjects/', views.getObjects),


]