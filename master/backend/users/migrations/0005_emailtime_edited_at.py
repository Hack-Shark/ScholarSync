# Generated by Django 4.2.1 on 2023-06-22 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_emailtime_freq'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtime',
            name='edited_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]