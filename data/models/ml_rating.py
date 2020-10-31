from django.db import models


class MlRating(models.Model):
    doc_id = models.IntegerField()
    reader_id = models.IntegerField()
    rating = models.FloatField()
