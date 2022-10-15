from webpage_extractor import *
from url_to_html import *
from html_to_text import *
import requests
import sys


def main():
    print(sys.argv[1])
    urls = open("output.txt", "w")
    urls = webpage_extractor(str(sys.argv[1]))
    open(urls)
    for url in urls:
        print(url)


if __name__ == '__main__':
    main()
