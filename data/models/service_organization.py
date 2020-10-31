from django.db import models


class ServiceOrganization(models.Model):
    full_name = models.TextField()
    short_name = models.TextField()
    street_name = models.TextField(null=True)
    underground_name = models.TextField(null=True)
