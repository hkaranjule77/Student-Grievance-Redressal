# Generated by Django 3.0.6 on 2020-06-04 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complain', '0003_auto_20200603_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='registered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 4, 12, 39, 50, 796456)),
        ),
    ]