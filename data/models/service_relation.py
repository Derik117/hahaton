from django.db import models


class ServiceRelation(models.Model):
    status = models.FloatField(null=True)
    service_user = models.ForeignKey('data.ServiceUser', null=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(null=True)
    organization = models.ForeignKey('data.ServiceOrganization', on_delete=models.DO_NOTHING)
    request = models.ForeignKey('data.ServiceRequest', null=True, on_delete=models.DO_NOTHING)
    service = models.ForeignKey('data.Service', null=True, on_delete=models.DO_NOTHING)
    enrolment_at = models.DateTimeField(null=True)
    expulsion_at = models.DateTimeField(null=True)
    reason = models.TextField(null=True)
    next_service_relation = models.ForeignKey('data.ServiceRelation', null=True, on_delete=models.DO_NOTHING,
                                              related_name='next_service_relations')
    prev_service_relation = models.ForeignKey('data.ServiceRelation', null=True, on_delete=models.DO_NOTHING,
                                              related_name='prev_service_relations')
    planned_start_date = models.DateField(null=True)
    planned_end_date = models.DateField(null=True)
