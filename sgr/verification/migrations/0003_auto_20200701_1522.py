# Generated by Django 3.0.6 on 2020-07-01 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0002_auto_20200701_1451'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tabledetail',
            old_name='first_name_col_name',
            new_name='firstname_col_name',
        ),
        migrations.RenameField(
            model_name='tabledetail',
            old_name='last_name_col_name',
            new_name='lastname_col_name',
        ),
    ]
