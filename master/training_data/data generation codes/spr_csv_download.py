from bs4 import BeautifulSoup
import time
import requests

start_time = time.time()
fail_path = 'failed.csv'
articles_path = 'articles.csv'
request_failed = 'request_failed.csv'
request_passed = 'request_passed.csv'


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
    page = soup.find("form", attrs={'class': 'pagination'})
    if not page:
        return
    else:
        if not page.find("img", attrs={'alt': 'next disabled'}):
            url = "https://link.springer.com" + \
                (page.find("a", attrs={'class': 'next'})).get('href')
            return url
        else:
            return None


def downloadlink_extract(url, alp, j):
    webpage = responser(url)
    if webpage is None:
        return
    soup = BeautifulSoup(webpage.content, "html.parser")
    links = soup.find_all("a", attrs={'class': 'c-atoz-list__link'})

    for i, x in enumerate(links):
        l = x.get('href')
        articles = responser(l)
        if articles is not None:
            soup = BeautifulSoup(articles.content, "html.parser")
            title = soup.find('title').text
            open_articles = soup.find_all(
                "a", attrs={'data-track-action': 'click open access articles'})
            if open_articles:
                link = open_articles[0].get('href')
                # print(link)
                csv_link = link.rsplit('?', 1)
                # print(csv_link)
                download_href = f"{csv_link[0]}/csv?{csv_link[1]}"
                # print(download_href)
                csv_data(download_href, alp, j, i, title)


def csv_data(download_links, alp, j, i, title):
    if download_links is None:
        return
    response = responser(download_links)

    # Check if the request was successful
    if response is not None:
        # Extract filename from the download link
        filename = f"{alp}_{j}.csv"

        # Decode the response content as text
        content = response.content.decode('utf-8')

        # Split the content into lines
        lines = content.splitlines()

        # Remove the first line if it exists
        if len(lines) > 0:
            lines = lines[1:]

        # Join the lines back into a single string
        content = '\n'.join(lines)

        # Save the downloaded file content to the output file
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            file.write(content)

        print(f"File downloaded successfully, link_no:{i+1}.{title}")
    else:
        print(f"Failed to download the file. {download_links.split('-')[-1]}")


def iter():
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(len(alpha)):
        for j in range(1, 5):
            alp = alpha[i]
            url = f"https://link.springer.com/journals/{alp}/{j}"
            downloadlink_extract(url, alp, j)
            print(i, j)
            print(time.time()-start_time)


iter()
