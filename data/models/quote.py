from django.db import models


class Quote(models.Model):
    text = models.TextField(null=True)
    book = models.ForeignKey('data.Catalog', on_delete=models.DO_NOTHING)
    rating = models.IntegerField(null=True)
