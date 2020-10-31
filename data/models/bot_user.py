from django.db import models


class BotUser(models.Model):
    reader = models.ForeignKey('data.Reader', on_delete=models.DO_NOTHING)
    tg_id = models.IntegerField()
