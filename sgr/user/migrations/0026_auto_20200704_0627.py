# Generated by Django 3.0.6 on 2020-07-04 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_auto_20200703_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='deact_requested_mem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Member'),
        ),
        migrations.AlterField(
            model_name='member',
            name='deactivated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_deactivated_by', to='user.Member'),
        ),
        migrations.AlterField(
            model_name='student',
            name='deact_requested_mem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deactivation_requested_member', to='user.Member'),
        ),
        migrations.AlterField(
            model_name='student',
            name='deactivated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_deactivated_by', to='user.Member'),
        ),
    ]
