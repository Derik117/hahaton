from django.db import models


class BookTake(models.Model):
    reader = models.ForeignKey('data.Reader', on_delete=models.DO_NOTHING)
    number = models.TextField()
    barcode = models.BigIntegerField()
    take_at = models.DateTimeField()
    return_at = models.DateTimeField()
    condition = models.ForeignKey()