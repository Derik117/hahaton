from django.db import models


class Event(models.Model):
    mosru_id = models.TextField()
    name = models.TextField()
    status = models.TextField()
    host_name = models.TextField()
    host_type = models.TextField()
    host_subclass = models.TextField(null=True)
    price = models.TextField(null=True)
    event_type = models.TextField()
    event_focus = models.TextField(null=True)
    is_holiday = models.TextField(null=True)
    holiday_name = models.TextField(null=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    description = models.TextField()
    is_online = models.TextField()
    address = models.TextField(null=True)
    district = models.TextField(null=True)
    area = models.TextField(null=True)
    is_disabled_friendly = models.TextField(null=True)
    disability_type = models.TextField(null=True)
    age_limit = models.IntegerField()
    age_group = models.TextField()
    target_audience = models.TextField(null=True)
    age_group_floor = models.IntegerField()
    age_group_ceil = models.IntegerField()
