from django.db import models
import uuid
import random
import string
import time
from django.utils import timezone

def generate_random_string(length=7):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(max_length=200, blank=False, null=False)
    password = models.CharField(max_length=200, blank=False, null=False)
    username = models.CharField(max_length=200, blank=False, null=False)
    name = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=250, blank=True, null=True)
    profile_image = models.TextField(null=True, blank=True)
    referal_link = models.CharField(max_length=8, default=generate_random_string, unique=True, editable=False)
    number_people = models.IntegerField(default=0)
    balance_usdt = models.FloatField(default=0.0)
    balance_netbo = models.FloatField(default=0.0)
    last_mining = models.IntegerField(default=0, null=True, blank=True)
    wallet_id_usdt = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    wallet_id_netbo = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_identified = models.BooleanField(default=False,null=True, blank=True)
    is_verified = models.IntegerField(null=True, blank=True)
    is_archived = models.IntegerField(null=True, blank=True)
    mac_address = models.CharField(max_length = 200, blank=True, null=True)
    # new
    friend_referal_link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.username
    
class Transaction(models.Model):
    profile_id = models.CharField(max_length=200, null=True, blank=True)
    balance_usdt = models.FloatField(default=0.0)
    balance_netbo = models.FloatField(default=0.0)
    created_at = models.IntegerField()

class Identified(models.Model):
    user_id = models.CharField(max_length=252)
    fullname = models.CharField(max_length=255)
    birthday = models.CharField(max_length=250)
    serial_document = models.CharField(max_length=255)
    id_image = models.TextField()
    address_image = models.TextField()
    selfie_image = models.TextField()
    is_identified = models.BooleanField(null=True, blank=True)

class MoneyOut(models.Model):
    profile_id = models.CharField(max_length=200, null=True, blank=True)
    wallet_addres = models.CharField(max_length=200, null=True, blank=True)
    balance_netbo = models.FloatField(default=0.0)
    is_identified = models.BooleanField(null=True, blank=True)
    created_at = models.IntegerField()

    def __str__(self) -> str:
        return self.profile_id

  

