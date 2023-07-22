from django.db import models
from django.contrib.auth.models import User
from datetime import date
import uuid 
from django.core.validators import MinValueValidator, MaxValueValidator

class Preference(models.Model):
    user=models.ForeignKey(User,related_name='user_pref',on_delete=models.CASCADE)
    text=models.CharField(max_length=100,blank=False)
    id=models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    created_at= models.DateField(default=date.today)
    # after = models.IntegerField(blank=False, validators=[MinValueValidator(1900), MaxValueValidator(9999)])

    def __str__(self):
        return f'{self.user}\t{self.text}\t'
    

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


class SpringerData(models.Model):
    item_title = models.CharField(null=False,default="",max_length=10000)
    publication_title = models.CharField(null=False,default="",max_length=10000)
    item_doi=models.CharField(primary_key=True,max_length=500)
    authors = models.TextField(null=True)
    publication_year = models.PositiveIntegerField(null=True)
    url = models.URLField()
    keywords = models.TextField(null=True)
    
    def _str_(self):
        return f'{self.item_title}\t{self.publication_title}'