from bs4 import BeautifulSoup
import requests
import pandas as pd

def getdata(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

def getnextpage(soup):
    page = soup.find("form", attrs={'class' : 'pagination'})
    if not page:
        return
    else:
        if not page.find("img", attrs={'alt':'next disabled'}):
            url ="https://link.springer.com" + (page.find("a", attrs={'class':'next'})).get('href')
            return url
        else:
            return
        
article_data=[]

url = "https://link.springer.com/journals/a/1"

webpage = requests.get(url)

soup = BeautifulSoup(webpage.content, "html.parser")

links = soup.find_all("a", attrs={'class' : 'c-atoz-list__link'})

for x in links:
    link = x.get('href')
    articles = requests.get(link)
    soup = BeautifulSoup(articles.content, "html.parser")
    open_articles = soup.find_all("a", attrs={'data-track-action' : 'click open access articles'})
    if open_articles:
        link = open_articles[0].get('href')
        while True:
            soup = getdata(link)
            article_links_data = soup.find_all("a", attrs={'class' : 'title'})
            for y in article_links_data:
                article_data.append(y.get('href'))
            link = getnextpage(soup)
            if not link:
                break

for i in range(len(article_data)):
    print(article_data[i])
    print()