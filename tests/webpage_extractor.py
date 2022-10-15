import requests
from bs4 import BeautifulSoup


def webpage_extractor(url):
    grab = requests.get(url)
    soup = BeautifulSoup(grab.text, 'html.parser'

    # opening a file in write mode
    f = open("webpages.txt", "w")
    # traverse paragraphs from soup
    for link in soup.find_all("a"):
        data = link.get('href')
        f.write(url + data)
        f.write("\n")

    return f
