from rest_framework import serializers
from main import models
from main.models import Account

class RegistrationSerializer(serializers.ModelSerializer):

	password2	= serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = models.Account
		fields = ['email', 'username', 'password', 'password2']
		extra_kwargs = {
				'password': {'write_only': True},
		}	

	def	save(self):

		account = Account(
					email=self.validated_data['email'],
					username=self.validated_data['username']
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		account.set_password(password)
		account.save()
		return account
        
class AccountSerializer(serializers.ModelSerializer):
  class Meta:
    object = serializers.StringRelatedField(many=True)
    fields = (
      'id',
      'email',
      'username',
      'name',
      'is_prosumer',
      'consuming',
      'producing',
      'address',
      'todays_energy_mix',
      'energy_mix_per_day',
      'overall_energy_mix',
      'object',
    )
    depth = 1
    model = models.Account


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'address',
            'consuming',
            'producing'
        )
        model = models.Account

class ContractSerializer(serializers.ModelSerializer):
  class Meta:
    fields = (
      'id',
      'name',
      'address',
    )
    model = models.Contract

class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
      fields = (
        'id',
        'is_consuming_object',
        'type',
        'owner',
        'energy_per_minute',
        'is_on',
        'overall_energy',
        'overall_expense',
        'number',
        'room',
        'model_reference',
        'name',
        'is_active',
        'energy_per_day',
        'todays_energy',
        'expense_per_day',
        'todays_expense',
      )
      model = models.Object

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'user',
            'transactions',
        )
        model = models.Transactions