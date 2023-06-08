from bs4 import BeautifulSoup
import time 
import requests
import re
start_time=time.time()
fail_path='failed.csv'
articles_path='articles.csv'
request_failed='request_failed.csv'
request_passed='request_passed.csv'
pattern=r'[^a-zA-Z0-9\s]'
def attach(string):
    x=string.splitlines()
    str=''.join(x)
    text=re.sub(pattern, '', str)
    modified_string = re.sub(r'\s+', ' ', text.strip())
    return modified_string

def responser(url):
    try:
        response = requests.get(url)
        # with open(request_passed, "a", encoding="utf-8") as f:
        #     f.write(f'{url}\n')   
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

            # Find the specific meta tag with name="keywords"
            meta_tag = soup.find('meta', attrs={'name': 'keywords'})
            # Find the specific div tag with abstract
            data = soup.find('div',attrs={'class':'app-promo-text app-promo-text--keyline'})

            # Extract the content from the meta tag
            if meta_tag:
                keywords_content = meta_tag.get('content')
                # print(keywords_content)
            else:
                keywords_content=""
            if data is not None:
                abstract = data.get_text(separator=" ")
            else:
                abstract=""
            # print(abstract,keywords_content)
            with open(f'{alp}.csv', "a", encoding="utf-8") as f:

                f.write(f"{attach(x.get_text())};{attach(keywords_content)};{attach(abstract)}\n")


def iter():
    alpha=''
    for i in range(len(alpha)):
        for j in range(1,5):
            alp=alpha[i]
            url=f"https://link.springer.com/journals/{alp}/{j}"
            extract_articles(url,alp)
            print(i,j)
            print(time.time()-start_time)

iter()


