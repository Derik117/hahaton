from django.db import models


class PredictionCounter(models.Model):
    book = models.ForeignKey('data.Catalog', on_delete=models.DO_NOTHING)
    preds_number = models.IntegerField(null=True)
