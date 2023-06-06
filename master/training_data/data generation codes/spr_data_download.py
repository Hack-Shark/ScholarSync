from bs4 import BeautifulSoup
import time
import requests

start_time = time.time()
fail_path = 'failed.csv'
articles_path = 'articles.csv'
request_failed = 'request_failed.csv'
request_passed = 'request_passed.csv'

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

d_links = []
def extract_articles(url, alp,j):
    webpage = responser(url)
    if webpage is None:
        return
    soup = BeautifulSoup(webpage.content, "html.parser")
    links = soup.find_all("a", attrs={'class': 'c-atoz-list__link'})
    for x in links:
        link_href = x.get('href')
        print(link_href)
        link=link_href.rsplit('/', 1)
        download_href = "https://link.springer.com/search/csv?query=&search-within=Journal&package=openaccessarticles&facet-journal-id=" +link[-1]
        d_links.append(download_href)
    print(len(d_links))
    download_csv(d_links,alp,j)


# URL of the download link
# https://link.springer.com/journal/10530
# download_link = 'https://link.springer.com/search/csv?query=&search-within=Journal&package=openaccessarticles&facet-journal-id=10530'
def download_csv(download_links,alp,j):
    if download_links is None:
        return
    for i,download_link in enumerate(download_links):
        # if i<=65: continue
        # Send an HTTP GET request to the download link
        response = responser(download_link)
        # response = requests.get(download_link)

        # Check if the request was successful (status code 200)
        if response is not None:
            # Extract filename from the download link
            filename = f"{alp}_{j}.csv"

            # Decode the response content as text
            content = response.content.decode('utf-8')

            # Split the content into lines
            lines = content.splitlines()

            # Remove the first line if it exists and it's not the first file
            if i > 0 and len(lines) > 0:
                lines = lines[1:]

            # Join the lines back into a single string
            content = '\n'.join(lines)

            # Save the downloaded file content to the output file
            with open(filename, 'a', newline='', encoding='utf-8') as file:
                file.write(content)

            print(f"File downloaded successfully, i={i}")
        else:
            print(f"Failed to download the file. {download_link.split('-')[-1]}")
        # exit()


def iter():
    alpha='cdefghijklmnopqrstuvwxyz'
    # alpha = 'b'
    for i in range(len(alpha)):
        for j in range(1,5):
            alp = alpha[i]
            url = f"https://link.springer.com/journals/{alp}/{j}"
            extract_articles(url, alp,j)
            print(i, j)
            print(time.time()-start_time)

    # for i in range(len(alpha)):
    #     alp = alpha[i]
    #     url = f"https://link.springer.com/journals/{alp}/2"
    #     extract_articles(url, alp,2)
    #     print(i, 2)
    #     print(time.time()-start_time)


iter()
