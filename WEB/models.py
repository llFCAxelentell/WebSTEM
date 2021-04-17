from django.db import models


# Create your models here.

class Reto(models.Model):
    nombre = models.CharField(max_length =30)
    minutos_jugados =models.IntegerField()


class Usuario(models.Model):
    names = models.CharField(max_length =30)
    last_names = models.CharField(max_length =30)
    created = models.CharField(max_length =30)
    email = models.CharField(max_length =30)
    password = models.CharField(max_length =255)
    username = models.CharField(max_length =30)
    gender = models.CharField(max_length =30)
    birthdate = models.CharField(max_length =30)


class Sesion(models.Model):
    user_id = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True)
    started = models.CharField(max_length =30)
    ended = models.CharField(max_length =30)


class Try(models.Model):
    session_id = models.ForeignKey(Sesion, on_delete=models.SET_NULL, blank=True, null=True)
    try_num = models.IntegerField()
    debt = models.IntegerField()

class Day(models.Model):
    try_id = models.ForeignKey(Try, on_delete=models.SET_NULL, blank=True, null=True)
    dayNumer = models.IntegerField()
    success = models.IntegerField()
    num_compounds_made = models.IntegerField()
    num_compounds_sold = models.IntegerField()
    num_elements_purchased = models.IntegerField()
    customers_rejected = models.IntegerField()
    money_generated_day = models.IntegerField()
