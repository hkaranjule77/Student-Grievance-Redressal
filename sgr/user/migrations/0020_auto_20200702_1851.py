# Generated by Django 3.0.6 on 2020-07-02 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_auto_20200701_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='deact_requested_mem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Member'),
        ),
        migrations.AddField(
            model_name='member',
            name='deactivated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_deactivated_by', to='user.Member'),
        ),
        migrations.AddField(
            model_name='member',
            name='deactivation_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='deact_requested_mem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deactivation_requested_member', to='user.Member'),
        ),
        migrations.AddField(
            model_name='student',
            name='deactivated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_deactivated_by', to='user.Member'),
        ),
        migrations.AddField(
            model_name='student',
            name='deactivation_reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]