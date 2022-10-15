from bs4 import BeautifulSoup
import requests

page = requests.get("https://www.westalabamaaging.org/bibb-county-centers-1")
soup = BeautifulSoup(page.content, 'html.parser')

for div in soup.find_all("div", {'class':'horizontal-navigation-bar clear with-logo'}):
    div.decompose()

soup.find("div", id="sidebar-one").decompose()
soup.find("div", id="page-footer").decompose()
soup.find("nav", id="mobile-navigation").decompose()


print(soup.prettify())

with open("beautifulsoupoutput1.html", "w") as file:
    file.write(str(soup))

