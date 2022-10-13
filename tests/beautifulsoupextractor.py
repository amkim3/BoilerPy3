from bs4 import BeautifulSoup
import requests

page = requests.get("https://www.westalabamaaging.org/bibb-county-centers-1")
soup = BeautifulSoup(page.content, 'html.parser')

for div in soup.find_all("div", {'class':'horizontal-navigation-bar clear with-logo'}):
    div.decompose()

for div in soup.find_all("div", {'id':'sidebar-one' or 'page-footer'}):
    div.decompose()


print(soup.prettify())

# with open("beautifulsoupoutput.html", "w") as file:
#     file.write(str(soup))

