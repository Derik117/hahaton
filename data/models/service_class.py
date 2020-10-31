from django.db import models


class ServiceClass(models.Model):
    parent = models.ForeignKey('data.ServiceClass',
                               null=True,
                               on_delete=models.DO_NOTHING)
    name = models.TextField()
