import sys
import requests
import unicodedata
from bs4 import BeautifulSoup
from boilerpy3 import extractors


# Function to grab all the webpages related to a site
def webpage_extractor(url):
    grab = requests.get(url)
    soup = BeautifulSoup(grab.text, 'html.parser')

    # opening a file in write mode
    f = open("../tests/webpages.txt", "w")
    # traverse paragraphs from soup
    for link in soup.find_all("a"):
        data = link.get('href')
        f.write(url + data)
        f.write("\n")

    return open("../tests/webpages.txt", mode='r', encoding='utf-8')


# function to return the html of each page, without headers, sidebar, or footers
# Returns the title of the file
def get_html(url):
    page = requests.get(str(url))  # request url
    soup = BeautifulSoup(page.content, 'html.parser')  # get html from url using html.parser
    # with open("../tests/hehetest.txt", "w") as f:
    #     f.write(soup.prettify())

    # to get rid of navigation panel on top of page
    for div in soup.find_all("div", {'class': 'horizontal-navigation-bar clear with-logo'}):
        div.decompose()

    # get rid of sidebar
    for div in soup.find_all("div", id="sidebar-one"):
        div.decompose()

    # get rid of page footer
    for div in soup.find_all("div", id="page-footer"):
        div.decompose()
    for br in soup.find_all("br"):
        br.replace_with(" ")

    soup.find("nav", id="mobile-navigation").decompose()

    title = soup.title.get_text()
    title = ''.join(char if char.isalnum() else '_' for char in title)
    with open('%s.html' % title, "w") as file:
        file.write(str(soup))
    file.close()
    return title


def main():
    # Extract webpages
    urls = webpage_extractor(str(sys.argv[1]))

    # Loop through
    count = 0
    for url in urls:
        if count == 1:
            url = url.replace("\n", "") # Otherwise code will not work
            # call get_html
            url = "https://www.westalabamaaging.org/alabama-farmers-market-program"
            title = get_html(url)
            # extract text
            extractor = extractors.KeepEverythingExtractor() # Boilerpipe "keep everything" extractor
            # write text to text file
            with open("%s.txt" % title, "w+") as f:
                text = extractor.get_content_from_file('%s.html' % title)
                # f.write(extractor.get_content_from_file('%s.html' % title))
                clean_text = unicodedata.normalize("NFKD", text)
                # print(clean
                f.write(clean_text)
                # filedata = f.read()
                # filedata = filedata.replace('\xa0', ' ')
                # f.write(filedata)
            f.close()

            break
        else:
            count += 1


if __name__ == '__main__':
    main()
