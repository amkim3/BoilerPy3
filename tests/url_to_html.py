from bs4 import BeautifulSoup
import requests


class File:
    def __init__(self, title, file):
        self.title = title
        self.contents = file


def get_html(url):
    page = requests.get(url)  # request url
    soup = BeautifulSoup(page.content, 'html.parser')  # get html from url using html.parser

    with open("testlmao.txt", "w") as f:
        f.write(soup.prettify())
    # to get rid of navigation panel on top of page
    for div in soup.find_all("div", {'class': 'horizontal-navigation-bar clear with-logo'}):
        div.decompose()

    # get rid of side bar
    for div in soup.find_all("div", id="sidebar-one"):
        div.decompose()

    # get rid of page footer
    for div in soup.find_all("div", id="page-footer"):
        div.decompose()

    # get rid of mobile navigation code
    for nav in soup.find_all("nav", id="mobile-navigation"):
        nav.decompose()

    # extract title
    # title = soup.find('title').get_text()
    # title.replace(" ", "_")
    # print(title)
    print(url)
    title = soup.title.get_text()
    print(title)

    with open('%s.html' % title, "w") as file:
        file.write(str(soup))
    file.close()

    # output = File("%s" % title, "%s.html" % title)
    # output.title = title
    # print(output.title)
    # output.contents = open('%s.html' % output.title, mode='r', encoding='utf-8')

    return output
