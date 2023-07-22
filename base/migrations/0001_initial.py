# Generated by Django 4.2.1 on 2023-07-20 00:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.IntegerField()),
                ('journal_id', models.IntegerField()),
                ('article_abstract', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CombinedText',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='combined_text', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('combined_text', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpringerData',
            fields=[
                ('item_title', models.CharField(default='', max_length=10000)),
                ('publication_title', models.CharField(default='', max_length=10000)),
                ('item_doi', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('authors', models.TextField(null=True)),
                ('publication_year', models.PositiveIntegerField(null=True)),
                ('url', models.URLField()),
                ('keywords', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('text', models.CharField(max_length=100)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_pref', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='article',
            constraint=models.UniqueConstraint(fields=('article_id', 'journal_id'), name='unique_article_journal'),
        ),
        migrations.AddConstraint(
            model_name='userarticle',
            constraint=models.UniqueConstraint(fields=('user', 'article'), name='unique_user_article_journal'),
        ),
    ]
