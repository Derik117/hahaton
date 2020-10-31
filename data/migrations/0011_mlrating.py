# Generated by Django 3.1.2 on 2020-10-31 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_mlbook'),
    ]

    operations = [
        migrations.CreateModel(
            name='MlRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_id', models.IntegerField()),
                ('reader_id', models.IntegerField()),
                ('rating', models.FloatField()),
            ],
        ),
    ]