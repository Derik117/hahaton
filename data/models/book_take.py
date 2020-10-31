from django.db import models


class BookTake(models.Model):
    reader = models.ForeignKey('data.Reader', on_delete=models.DO_NOTHING)
    inventory_id = models.TextField()
    barcode = models.BigIntegerField()
    take_at = models.DateTimeField()
    return_at = models.DateTimeField()
    condition = models.ForeignKey('data.Condition', on_delete=models.DO_NOTHING)
