# Generated by Django 3.0.6 on 2020-07-01 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_memberidcount_next_principal_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='deactivation_request',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='deactivation_request',
            field=models.BooleanField(default=False),
        ),
    ]