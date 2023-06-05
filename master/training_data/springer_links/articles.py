from bs4 import BeautifulSoup
import requests
import os
import time 
import requests
from requests.exceptions import ReadTimeout

start_time=time.time()
fail_path='failed.csv'
articles_path='articles.csv'
request_failed='request_failed.csv'
request_passed='request_passed.csv'
def attach(string):
    return ''.join(string.splitlines())
def responser(url):
    try:
        response = requests.get(url)
        with open(request_passed, "a", encoding="utf-8") as f:
            f.write(f'{url}\n')   
        return response
    except requests.exceptions.Timeout as e:
        print("Timeout exception occurred:", e)
        with open(request_failed, "a", encoding="utf-8") as f:
            f.write(f'{url}\n')  
        return None
    except requests.exceptions.ConnectionError as e:
        print("ConnectionError exception occurred:", e)
        with open(request_failed, "a", encoding="utf-8") as f:
            f.write(f'{url}\n') 
        return None
    except requests.exceptions.HTTPError as e:
        print("HTTPError exception occurred:", e)
        with open(request_failed, "a", encoding="utf-8") as f:
            f.write(f'{url}\n') 
        return None
    except requests.exceptions.RequestException as e:
        print("RequestException occurred:", e)
        with open(request_failed, "a", encoding="utf-8") as f:
            f.write(f'{url}\n') 
        return None
    except Exception as e:
        print("An unexpected exception occurred:", e)
        with open(request_failed, "a", encoding="utf-8") as f:
            f.write(f'{url}\n') 
        return None

def getdata(url):
    r = responser(url)
    if r is not None:
        soup = BeautifulSoup(r.content, "html.parser")
        return soup
    else:
        return None

def getnextpage(soup):
    page = soup.find("form", attrs={'class' : 'pagination'})
    if not page:
        return
    else:
        if not page.find("img", attrs={'alt':'next disabled'}):
            url ="https://link.springer.com" + (page.find("a", attrs={'class':'next'})).get('href')
            return url
        else:
            return None

def extract_articles(url,alp):
    webpage = responser(url)
    if webpage is None:
        return
    soup = BeautifulSoup(webpage.content, "html.parser")
    links = soup.find_all("a", attrs={'class' : 'c-atoz-list__link'})
    for x in links:
        link = x.get('href')
        articles = responser(link)
        if articles is not None:
            soup = BeautifulSoup(articles.content, "html.parser")
            open_articles = soup.find_all("a", attrs={'data-track-action' : 'click open access articles'})
            if open_articles:
                link = open_articles[0].get('href')
                while True:
                    soup = getdata(link)
                    if soup is not None:
                        article_links_data = soup.find_all("a", attrs={'class' : 'title'})
                        for y in article_links_data:
                            with open(f'{alp}.csv', "a", encoding="utf-8") as f:
                                f.write(f"{attach(x.get_text())}||{attach(y.get_text())}||https://link.springer.com{attach(y.get('href'))}\n")
                        link = getnextpage(soup)
                        if not link:
                            break
                    else:
                        break
            else:
                x=str(x)
                soup = BeautifulSoup(x, 'html.parser')
                link_text = soup.a.get('href')
                with open(fail_path, "a", encoding="utf-8") as f:
                    f.write(f'{soup.a.get_text()}||{link_text}\n')   


def iter():
    alpha='j'
    for i in range(0,25):
        for j in range(3,5):
            alp=alpha[i]
            url=f"https://link.springer.com/journals/{alp}/{j}"
            extract_articles(url,alp)
            print(i,j)
            print(time.time()-start_time)
            
        
iter()


