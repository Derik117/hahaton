from django.db import models


class Reader(models.Model):
    birth_date = models.DateField()
    age = models.FloatField()