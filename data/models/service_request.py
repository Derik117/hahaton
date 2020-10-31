from django.db import models


class ServiceRequest(models.Model):
    status = models.TextField()
    created_at = models.DateTimeField()
    rating = models.FloatField()
    challenge_complete = models.BooleanField(null=True)
    accepted = models.BooleanField(null=True)
    declined = models.BooleanField(null=True)
    decline_reason = models.TextField(null=True)
    service = models.ForeignKey('data.Service', on_delete=models.DO_NOTHING)
