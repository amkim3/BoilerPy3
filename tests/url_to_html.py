from bs4 import BeautifulSoup
import requests


def get_html(url):
    page = requests.get(url)  # request url
    soup = BeautifulSoup(page.content, 'html.parser')  # get html from url using html.parser

    # to get rid of navigation panel on top of page
    for div in soup.find_all("div", {'class': 'horizontal-navigation-bar clear with-logo'}):
        div.decompose()

    # get rid of side bar
    soup.find("div", id="sidebar-one").decompose()

    # get rid of page footer
    soup.find("div", id="page-footer").decompose()

    # get rid of mobile navigation code
    soup.find("nav", id="mobile-navigation").decompose()

    with open("urlToHtmlOutput.html", "w") as file:
        file.write(str(soup))
    file.close()
    return file
