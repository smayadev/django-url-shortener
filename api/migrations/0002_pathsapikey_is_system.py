# Generated by Django 5.1.5 on 2025-02-23 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pathsapikey',
            name='is_system',
            field=models.BooleanField(default=False),
        ),
    ]
