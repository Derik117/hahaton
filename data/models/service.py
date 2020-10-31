from django.db import models


class Service(models.Model):
    finance_type = models.TextField()
    service_class = models.ForeignKey('data.ServiceClass', on_delete=models.DO_NOTHING)
    organization = models.ForeignKey('data.ServiceOrganization', on_delete=models.DO_NOTHING)
    schedule_type = models.TextField(null=True)
    service_name = models.TextField(null=True)
    created_at = models.DateTimeField(null=True)
    duration = models.TextField()
    duration_unit = models.TextField()
