# Generated by Django 3.0.6 on 2020-07-12 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complain', '0002_auto_20200712_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]