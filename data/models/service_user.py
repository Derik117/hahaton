from django.db import models


class ServiceUser(models.Model):
    age = models.FloatField()
    sex = models.TextField()
