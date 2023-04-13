import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField
from address.models import AddressField

# Create your models here.

class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an emain address')
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
              email=self.normalize_email(email),
              password=password,
              username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
      email = models.EmailField(verbose_name="email", max_length=60, unique=True)
      username = models.CharField(max_length=30, unique=True)
      date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
      last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
      is_admin = models.BooleanField(default=False)
      is_active = models.BooleanField(default=True)
      is_staff = models.BooleanField(default=False)
      is_superuser = models.BooleanField(default=False)

      is_new_user = models.BooleanField(default=False)

      name = models.CharField(verbose_name="Name", max_length=40, default="")
      is_prosumer = models.BooleanField(default=False)
      consuming = models.IntegerField(default=0)
      producing = models.IntegerField(default=0)
      eth_address = models.CharField(max_length=42, default="")
      private_key = models.CharField(max_length=70, default="")
      address = AddressField(blank=True,null=True)

      todays_energy_mix = ArrayField(models.IntegerField(), blank=True,default=list)
      energy_mix_per_day = ArrayField(ArrayField(models.IntegerField(), blank=True,default=list), blank=True, default=list)
      overall_energy_mix = ArrayField(models.IntegerField(), blank=True, default=list)


      USERNAME_FIELD = 'email'
      REQUIRED_FIELDS = ['username']

      objects = MyAccountManager()

      def __str__(self):
        return self.username
      
      def has_perm(self, perm, obj=None):
        return self.is_admin

      def has_module_perms(self, app_label):
        return True
      
class Object(models.Model):
      TYPE_CHOICES = (("SOLAR_PANEL", 'solar_panel'), ("WIND_TURBINE", 'wind_turbine'), ("HEATING", 'heating'), ("COOLING", 'cooling'), ("TV", 'tv'), ("LIGHTING", 'lighting'), ("WASHER", 'washer'), ("DRYER", 'dryer'), ("REFREGIRATOR", 'refregirator'))

      is_consuming_object = models.BooleanField(default=True)
      type = models.CharField(max_length = 20, choices = TYPE_CHOICES, default = "HEATING")
      owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='object', blank=True, null=True)
      energy_per_minute = models.IntegerField(default=10)
      is_on = models.BooleanField(default=False)
      overall_energy = models.IntegerField(default=0)
      overall_expense = models.IntegerField(default=0)
      number = models.IntegerField(default=0)
      room = models.CharField(default='', max_length=50)
      model_reference = models.CharField(default='', max_length=50)
      name = models.CharField(default='', max_length=50)
      is_active = models.BooleanField(default=True)
      energy_per_day = ArrayField(models.IntegerField(), blank=True,default=list)
      todays_energy = models.IntegerField(default=0)
      expense_per_day = ArrayField(models.IntegerField(), blank=True,default=list)
      todays_expense = models.IntegerField(default=0)
      
      def __str__(self):
          return self.owner.name + "'s " + self.type

class Contract(models.Model):
      name = models.CharField(max_length=20, default='')
      address = models.CharField(max_length=42, default='')
      price = ArrayField(models.IntegerField(), blank=True, default=list)
      
      def __str__(self):
        return self.name
    
class Transactions(models.Model):
      user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions', blank=True, null=True)
      transactions = ArrayField(ArrayField(models.CharField(max_length=100), default=list, blank=True, null=True), default=list, blank=True, null=True)
      last_block = models.IntegerField(default=0)
      address = models.CharField(max_length=42, default='')