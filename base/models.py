from django.db import models
from django.contrib.auth.models import User
from datetime import date
import uuid 

class Preference(models.Model):
    user=models.ForeignKey(User,related_name='user_pref',on_delete=models.CASCADE)
    text=models.CharField(max_length=100,blank=False)
    id=models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    created_at= models.DateField(default=date.today)
    after= models.DateField(blank=False)
    def __str__(self):
        return f'{self.user}\t{self.text}\t{self.after}'
    

class CombinedText(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='combined_text', on_delete=models.CASCADE)
    combined_text = models.TextField(blank=True)
    def __str__(self):
        return f'{self.user}\t{self.combined_text}'


class Article(models.Model):
    article_id = models.IntegerField()
    journal_id = models.IntegerField()
    article_abstract = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['article_id', 'journal_id'], name='unique_article_journal')
        ]

    def __str__(self):
        return f'{self.journal_id}\t{self.article_id}\t{self.article_abstract[:25]}...'


class UserArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'], name='unique_user_article_journal')
        ]

    def __str__(self):
        return f'{self.user}\t{self.article}'

class JournalArticle(models.Model):
    title = models.CharField(null=True)
    publication_title = models.CharField(null=True)
    item_doi = models.CharField(primary_key=True)
    authors = models.CharField(null=True)
    publication_year = models.PositiveIntegerField(null=True)
    url = models.URLField()
    keywords = models.CharField(null=True)
    language = models.CharField(null=True)
