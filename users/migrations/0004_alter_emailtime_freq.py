# Generated by Django 4.2.1 on 2023-06-21 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_frequency_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtime',
            name='freq',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.frequency'),
        ),
    ]
