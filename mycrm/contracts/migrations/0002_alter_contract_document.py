# Generated by Django 5.0 on 2024-01-12 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='media/contracts/'),
        ),
    ]
