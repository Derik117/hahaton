from django.db import models


class BookCopy(models.Model):
    book = models.ForeignKey('data.Catalog', on_delete=models.DO_NOTHING)
    inventory_id = models.TextField()
    barcode = models.BigIntegerField()
    classification_id = models.TextField()
    sigles_id = models.FloatField()
