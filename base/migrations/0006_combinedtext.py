# Generated by Django 4.2.1 on 2023-06-20 05:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('base', '0005_delete_combinedtext'),
    ]

    operations = [
        migrations.CreateModel(
            name='CombinedText',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='combined_text', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('combined_text', models.TextField(blank=True)),
            ],
        ),
    ]
