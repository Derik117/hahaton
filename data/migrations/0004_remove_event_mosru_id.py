# Generated by Django 3.1.2 on 2020-10-31 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='mosru_id',
        ),
    ]