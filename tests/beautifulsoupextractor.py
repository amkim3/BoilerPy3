from bs4 import BeautifulSoup
import requests
import re
from boilerpy3 import extractors
import spacy
from spacy.pipeline import EntityRuler
from spacy.matcher import Matcher


class File:
    def __init__(self):
        self.title = ''
        self.contents = ''


page = requests.get("https://www.westalabamaaging.org/bibb-county-centers")
soup = BeautifulSoup(page.content, 'html.parser')

for div in soup.find_all("div", {'class': 'horizontal-navigation-bar clear with-logo'}):
    div.decompose()
#
# soup.find("div", id="sidebar-one").decompose()
# soup.find("div", id="page-footer").decompose()
soup.find("nav", id="mobile-navigation").decompose()
# for div in soup.find_all("div", {'class': 'horizontal-navigation-bar clear with-logo'}):
#     div.decompose()

# get rid of side bar
for div in soup.find_all("div", id="sidebar-one"):
    div.decompose()

# get rid of page footer
for div in soup.find_all("div", id="page-footer"):
    div.decompose()
title = soup.title.get_text()

for br in soup.find_all("br"):
    br.replace_with(" ")

# print(soup.prettify())
title = ''.join(char if char.isalnum() else '_' for char in title)
print(title)

with open('%s.html' % title, "w") as file:
    file.write(str(soup))
file.close()


extractor = extractors.KeepEverythingExtractor()
with open("test102622.txt", "w") as f:
    f.write(extractor.get_content_from_file('%s.html'%title))
f.close()

# pattern_tel = {"label": "TELEPHONE", "pattern": [
#     {"TEXT": {"REGEX": r"\(?\d{3}\)?"}},
#     {"TEXT": "-"},
#     {"TEXT": {"REGEX": r"\d{3}"}},
#     {"TEXT": "-"},
#     {"TEXT": {"REGEX": r"\d{4}"}}
#     ]}

phone_number = [{'SHAPE': 'ddd'},
            {'ORTH': '-'},
            {'SHAPE': 'ddd'},
            {'ORTH': '-', 'OP': '?'},
            {'ORTH': '-', 'OP': '?'},
            {'SHAPE': 'dddd'}]
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
matcher.add('Phonenumber',[phone_number])
# pattern = [[{"LIKE_EMAIL": True}], [{"POS": "PROPN"}]]
count = 0
with open("test102622.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        if count != 4:
            count += 1
            continue
        print(line)
        doc = nlp(line)
        matches = matcher(doc)
        for match_id, start, end in matches:
            print(doc[start:end])
        for ent in doc.ents:
            print(ent.text + ' - ' + ent.label_ + ' - ' + str(spacy.explain(ent.label_)))
        break





# output = File()
# output.title = title
# output.contents = open('%s.html' % title, mode='r', encoding='utf-8')
#
# print(output.title)
