import json
from django.test import Client, TestCase
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.urls import include, path, reverse
from rest_framework import status
from api.serializers import *
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from main.models import Account
# Create your tests here.

client = Client()

class GetAllAccountTest(TestCase):
    """ Test module for GET all accounts API """

    def setUp(self):
        Account.objects.create(
            name='Casper', username='Casper', email='casper@gmail.com', is_prosumer=True)
        Account.objects.create(
            name='Ben', username=1, email='ben@gmail.com', is_prosumer=False)
        Account.objects.create(
            name='John', username=2, email='john@gmail.com', is_prosumer=True)
        Account.objects.create(
            name='Bob', username=6, email='bob@gmail.com', is_prosumer=False)

    def test_get_all_accounts(self):
        # get API response
        response = client.get(reverse('accounts'))
        # get data from db
        account = Account.objects.all()
        serializer = AccountSerializer(account, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSingleAccountTest(TestCase):
    """ Test module for GET single Account API """

    def setUp(self):
        self.casper = Account.objects.create(
            name='Casper', username='Casper', email='casper@gmail.com', is_prosumer=True)
        self.Ben = Account.objects.create(
            name='Ben', username=1, email='ben@gmail.com', is_prosumer=False)
        self.John = Account.objects.create(
            name='John', username=2, email='john@gmail.com', is_prosumer=True)
        self.Bob = Account.objects.create(
            name='Bob', username=6, email='bob@gmail.com', is_prosumer=False)

    def test_get_valid_single_Account(self):
        response = client.get(
            reverse('account', kwargs={'pk': self.John.pk}))
        account = Account.objects.get(pk=self.John.pk)
        serializer = AccountSerializer(account)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_Account(self):
        response = client.get(
            reverse('account', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewAccountTest(TestCase):
    """ Test module for inserting a new Account """

    def setUp(self):
        self.valid_payload = {
            'name': 'Ben',
            'username': 'Ben 2',
            'email': 'ben2@gmail.com',
            'is_prosumer': True
        }
        self.invalid_payload = {
            'name': '',
            'username': 4,
            'email': 'Pamerion',
            'is_prosumer': 'White'
        }

    def test_create_valid_Account(self):
        response = client.post(
            reverse('updateAccount'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_Account(self):
        response = client.post(
            reverse('updateAccount'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleAccountTest(TestCase):
    """ Test module for updating an existing Account record """

    def setUp(self):
        self.casper = Account.objects.create(
            name='Casper', username='Casper', email='casper@gmail.com', is_prosumer=True)
        self.Ben = Account.objects.create(
            name='Sam', username='Sam', email='sam@gmail.com', is_prosumer=False)
        self.valid_payload = {
            'name': 'Ben',
            'username': 'Ben',
            'email': 'ben@gmail.com',
            'is_prosumer': True
        }
        self.invalid_payload = {
            'name': '',
            'username': 4,
            'email': 'Pamerion',
            'is_prosumer': False
        }

    def test_valid_update_Account(self):
        response = client.put(
            reverse('updateAccount', kwargs={'pk': self.Ben.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_Account(self):
        response = client.put(
            reverse('updateAccount', kwargs={'pk': self.Ben.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSingleAccountTest(TestCase):
    """ Test module for deleting an existing Account record """

    def setUp(self):
        self.casper = Account.objects.create(
            name='Casper', username='Casper', email='casper@gmail.com', is_prosumer=True)
        self.Ben = Account.objects.create(
            name='Ben', username='Ben', email='ben@gmail.com', is_prosumer=False)

    def test_valid_delete_Account(self):
        response = client.delete(
            reverse('deleteAccount', kwargs={'pk': self.Ben.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_Account(self):
        response = client.delete(
            reverse('deleteAccount', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class EnergyManagementTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a mock account and objects here

    def test_get_weekly_energy_mix(self):
        url = reverse('getWeeklyEnergyMix')  # Replace with the actual URL name if different
        data = {"id": self.mock_account.id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add any additional assertions for the response data

    def test_get_overall_energy_mix(self):
        url = reverse('getOverallEnergyMix')  # Replace with the actual URL name if different
        data = {"id": self.mock_account.id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add any additional assertions for the response data

    def test_change_profile_details(self):
        url = reverse('changeProfileDetails')  # Replace with the actual URL name if different
        data = {
            "id": self.mock_account.id,
            "energy_mix_per_day": [[10, 20, 30], [15, 25, 35]]
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add any additional assertions for the response data

    def test_create_object(self):
        url = reverse('createObject')  # Replace with the actual URL name if different
        data = {
            "owner": self.mock_account.id,
            "name": "Example Object",
            "is_consuming_object": True,
            "type": "HEATING",
            "consumption_per_minute": 10,
            "room": "Living Room",
            "reference": "ABC123"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add any additional assertions for the response data

    def test_switch_object_state(self):
        url = reverse('switchObjectState')  # Replace with the actual URL name if different
        data = {"id": self.mock_object.id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add any additional assertions for the response data

    def test_delete_object(self):
        url = reverse('deleteObject')  # Replace with the actual URL name if different
        data = {"id": self.mock_object.id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add any additional assertions for the response data

    def test_deactivate_object(self):
        url = reverse('desactivateObject')  # Replace with the actual URL name if different
        data = {"id": self.mock_object.id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add any additional assertions for the response data

TEST_USER_ID = 1
class ObjectTests(APITestCase):
    
    def test_get_objects_weekly_data2(self):
        url = reverse('getObjectsWeeklyData2')
        data = {'id': TEST_USER_ID, 'is_consuming_object': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_objects_expenses(self):
        url = reverse('getObjectsExpenses')
        data = {'id': TEST_USER_ID, 'is_consuming_object': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_objects_weekly_expenses(self):
        url = reverse('getObjectsWeeklyExpenses')
        data = {'id': TEST_USER_ID, 'is_consuming_object': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_objects_weekly_expenses2(self):
        url = reverse('getObjectsWeeklyExpenses2')
        data = {'id': TEST_USER_ID, 'is_consuming_object': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_balance_of(self):
        test_user = Account.objects.get(pk=TEST_USER_ID)
        url = reverse('getBalanceOf', kwargs={'username': test_user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_balance_of_test(self):
        url = reverse('getBalanceOfTest')
        test_user = Account.objects.get(pk=TEST_USER_ID)
        data = {'username': test_user.username}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deploy_contract(self):
        url = reverse('deployContract')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)