# Generated by Django 5.0 on 2024-01-07 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0002_alter_service_options_contract_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='validity_period',
        ),
    ]
