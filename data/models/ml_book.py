from django.db import models


class MlBook(models.Model):
    doc_id = models.IntegerField()
    author = models.TextField(null=True)
    title = models.TextField(null=True)
    city = models.TextField(null=True)
    publisher = models.TextField(null=True)
    year = models.TextField(null=True)
    series = models.TextField(null=True)
    tags = models.TextField(null=True)
    article = models.TextField(null=True)
    age_rating = models.TextField(null=True)
    mean = models.FloatField(null=True)
    count = models.FloatField(null=True)
    rating = models.FloatField(null=True)
