from django.db import models


class Catalog(models.Model):
    author = models.TextField(null=True)
    title = models.TextField(null=True)
    city = models.TextField(null=True)
    publisher = models.TextField(null=True)
    year = models.TextField(null=True)
    series = models.TextField(null=True)
    tags = models.TextField(null=True)
    article = models.TextField(null=True)
    age_rating = models.TextField(null=True)
