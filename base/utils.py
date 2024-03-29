import requests
from bs4 import BeautifulSoup
from .models import Article, UserArticle


def article_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    title = soup.find("h1", attrs={'class': 'c-article-title'}).text
    # Check if the abstract element exists
    abstract_element = soup.find("div", attrs={'id': 'Abs1-content'})
    abstract = abstract_element.find("p").text if abstract_element else ""
    authors = []
    author_tags = soup.find_all('a', attrs={'data-test': 'author-name'})
    for author_tag in author_tags:
        author_name = author_tag.text.strip()
        authors.append(author_name)
    published = soup.find('a',attrs={'data-track-action':"publication date"}).find('time').text
    download_link ="https://link.springer.com"+soup.find('a', attrs={'class': 'c-pdf-download__link'}).get('href')

    return ({'title': title, 'abstract': abstract, 'authors': authors, 'published_date': published, 'url': url, 'download_link': download_link})


def process_articles(links,user):
    processed_links = []

    for link in links:
        title, url, article_id, journal_id = link

        # Check if the article already exists in the Article model
        try:
            article = Article.objects.get(article_id=article_id, journal_id=journal_id)
        except Article.DoesNotExist:
            # Article doesn't exist, create a new entry
            print(url)
            article_info = article_data(url)
            if article_info['abstract'] == "" or None:
                continue  # Skip processing if the abstract is null
            article = Article.objects.create(article_id=article_id, journal_id=journal_id, article_abstract=article_info['abstract'])

        # Check if the article is associated with the user in the UserArticle model
        user_article_exists = UserArticle.objects.filter(user=user, article=article).exists()

        if not user_article_exists:
            # Article is not associated with the user, create a new entry in UserArticle model
            user_article = UserArticle.objects.create(user=user, article=article)
            processed_links.append(url)

        if len(processed_links) == 5:
            break

    return processed_links
