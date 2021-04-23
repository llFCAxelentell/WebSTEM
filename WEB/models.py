from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    names = models.CharField(max_length =30)
    last_names = models.CharField(max_length =30)
    created = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length =30)
    password = models.CharField(max_length =255)
    username = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    gender = models.CharField(max_length =30)
    birthdate = models.DateField(blank=True, null=True)

class Sesion(models.Model):
    user_id = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True)
    started = models.DateTimeField(blank=True, null=True)
    ended = models.DateTimeField(blank=True, null=True)

class Try(models.Model):
    session_id = models.ForeignKey(Sesion, on_delete=models.SET_NULL, blank=True, null=True)
    try_num = models.IntegerField()
    debt = models.IntegerField(blank=True, null=True)

class Day(models.Model):
    try_id = models.ForeignKey(Try, on_delete=models.SET_NULL, blank=True, null=True)
    day_number = models.IntegerField()
    success = models.BooleanField()
    num_compounds_made = models.IntegerField()
    num_compounds_sold = models.IntegerField()
    num_elements_purchased = models.IntegerField()
    customers_rejected = models.IntegerField()
    money_generated_day = models.IntegerField()
