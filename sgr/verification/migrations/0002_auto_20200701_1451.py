# Generated by Django 3.0.6 on 2020-07-01 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tabledetail',
            old_name='full_name_col_name',
            new_name='fullname_col_name',
        ),
        migrations.RemoveField(
            model_name='tabledetail',
            name='full_name_type',
        ),
    ]