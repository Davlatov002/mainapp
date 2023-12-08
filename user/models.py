from django.db import models
import uuid
import random
import string

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
    balance_usdt = models.FloatField(default=0.0)
    balance_netbo = models.FloatField(default=0.0)
    wallet_id_usdt = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    wallet_id_netbo = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_identified = models.BooleanField(default=False)
    is_verified = models.IntegerField(null=True, blank=True)
    is_archived = models.IntegerField(null=True, blank=True)
    mac_address = models.CharField(max_length = 200, blank=True, null=True)#

    def __str__(self) -> str:
        return self.username
    
class Transaction(models.Model):
    username = models.CharField(max_length=200, null=True, blank=True)
    balance_usdt = models.FloatField(default=0.0)
    balance_netbo = models.FloatField(default=0.0)
    balance_btc = models.FloatField(default=0.0)
    created_at = models.DateField(default=None, blank=True, null=True)

    def __str__(self) -> str:
        return self.username
