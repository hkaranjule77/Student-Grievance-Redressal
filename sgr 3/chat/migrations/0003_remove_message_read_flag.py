# Generated by Django 3.0.6 on 2020-07-18 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_message_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='read_flag',
        ),
    ]
