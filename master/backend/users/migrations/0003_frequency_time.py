# Generated by Django 4.2.1 on 2023-06-18 18:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_frequency_alter_emailtime_freq"),
    ]

    operations = [
        migrations.AddField(
            model_name="frequency",
            name="time",
            field=models.DurationField(default=datetime.timedelta(days=1)),
        ),
    ]
