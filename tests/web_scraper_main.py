from webpage_extractor import *
from url_to_html import *
from html_to_text import *
import requests
import sys


def main():
    # print(sys.argv[1])

    # open file to output webpage links to
    # urls = open("output.txt", "w")

    # webpage_extractor returns the links of all the webpages
    urls = webpage_extractor(str(sys.argv[1]))

    # for each url, call url_to_html to remove unnecessary classes
    count = 0
    for url in urls:
        # print(url)
        if count == 0:
            count += 1
            continue
        file = get_html(str(url))
        # print(file.title)
        # print(file.contents)
        # with open("testtt.txt", "w") as f:
        #     f.write(file.contents.read())
        #     print(file.contents.read())
        #     # print("penis")
        count += 1
        if count == 3: break


if __name__ == '__main__':
    main()
