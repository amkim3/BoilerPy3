# import pandas as pd
import spacy
from spacy import displacy
from spacy.tokens import DocBin
import json
from datetime import datetime
from tqdm import tqdm
import re
#
# nlp=spacy.load('en_core_web_sm')
# ner=nlp.get_pipe("ner")
#
# TRAIN_DATA = [
#     ("Brent Senior Activity Center 10445 AL-5 Brent, AL 35034 205-926-3968 Center Director:  Wanda Holder sacbrent@hotmail.com Open Monday - Friday  8:00 A.M. - 2:00 P.M.", {"entities": [(0,27, "ORG"), (29, 54, "ADDRESS"), (56,67, "PHONE"), (87, 98, "PERSON"),(100,119, "EMAIL"), (126, 163, "HOURS")]}),
#     ("Woodstock Senior Activity Center 28515 Hwy. 5 Woodstock, AL 35188 205-938-9790 Center Director:  Frankie Grammer Open Monday - Friday 9:00 A.M. - 1:00 P.M.", {"entities:" [(0,30, "ORG"), (32, 63, "ADDRESS"), (65, 76, "PHONE"), (96, 110, "PERSON"), (117, 153, "HOURS")]})
# ]

collective_dict = {'TRAINING_DATA': []}


def structure_training_data(text, kw_dict):
    results = []
    entities = []

    # search for instances of keywords within the text (ignoring letter case)
    for kw in tqdm(kw_dict.values()):
        for entry in kw:
            search = re.finditer(entry, text, flags=re.IGNORECASE)
            # store the start/end character positions
            all_instances = [[m.start(), m.end()] for m in search]

            # if the callable_iterator found matches, create an 'entities' list

            if len(all_instances) > 0:
                value = {i for i in kw_dict if kw_dict[i] == kw}
                for i in all_instances:
                    start = i[0]
                    end = i[1]
                    entities.append((start, end, value))

            # alert when no matches are found given the user inputs
            else:
                # print("No pattern matches found. Keyword:", kw)
                continue

    # add any found entities into a JSON format within collective_dict
    if len(entities) > 0:
        results = [text, {"entities": entities}]
        print(results)
        collective_dict['TRAINING_DATA'].append(results)
        return


nlp = spacy.blank('en')


def create_training_set(TRAIN_DATA):
    db = DocBin()
    for text, annot in tqdm(TRAIN_DATA):
        doc = nlp.make_doc(text)
        ents = []

        # create span objects
        for start, end, label in annot["entities"]:
            start.to_bytes(2, byteorder='big')
            end.to_bytes(2, byteorder='big')
            new = repr(label)
            # print(label)
            span = doc.char_span(start, end, label=new, alignment_mode="contract")

            # skip if the character indices do not map to a valid span
            if span is None:
                print("Skipping entity.")
            else:
                ents.append(span)
                # handle erroneous entity annotations by removing them
                try:
                    doc.ents = ents
                except:
                    # print("BAD SPAN:", span, "\n")
                    ents.pop()
        doc.ents = ents

        # pack Doc objects into DocBin
        db.add(doc)
    return db


def main():

    dic = {
        # "LOC": ["Bibb co.", "Fayette Co.", "Greene Co."],
        "ORG": ["Lamar Co. Farmers Market","Moundville Farmers Market", "Bibb Co. Farmers Market", "Fayette Co. Farmers Market", "Greene Co. Farmers Market", "United Farmers Market", "Tuscaloosa River Market", "Greensboro Farmers Market"],
        "ADDRESS": ["281 Columbus Ave. Vernon, AL 35592","39751 Hwy 69 Moundville, AL 35474", "268 Belcher St Centreville, AL 35042", "650 McConnell Loop Fayette, AL", "137 Furse Ave Eutaw, AL 35462", "Co Rd 18 & Co Rd 41 Forkland, AL", "1900 Jack Warner Pkwy Tuscaloosa, AL 35401", "Hwy 14 & Hwy 61 Greensboro, AL 36744"],
        "PHONE": ["205-695-7139","205-792-3614", "334-518-9049", "205-596-3904", "205-799-5204", "334-289-4645", "205-248-5296", "205-614-2069", "334-624-0080", "904-316-9192"],
        "HOURS": ["Tuesdays 4:00 p.m.–6:00 p.m. Saturdays 8:00 a.m.–11:00 a.m.","Tuesdays June - Sept. 3:00 P.M. - 6:00 P.M.","Saturdays May - Oct. 8:00 A.M. - 12:00 P.M.", "June Tues. & Saturdays 7:00 A.M. - Until Thursdays 4:00 P.M. - 7:00 P.M.", "Saturdays April - Sept. 8:00 A.M. - 12:00 P.M.", "Saturdays May - Oct. 10:00 A.M. - 3:00 P.M.", "Saturdays Year Round 7:00 A.M. - 12:00 P.M. Tuesdays  April - November 3:00 P.M. - 6:00 P.M.", "Fridays May - Sept. 7:00 A.M. - 1:00 P.M."],
        "WEBSITE": ["http://fma.alabama.gov/seniornutrition/", "http://www.npfarmersmarket.com", "http://www.tuscaloosarivermarket.com"]
    }
    with open("testingData.txt", "r") as f:
        data = f.read().splitlines()
        # count = 0
        for line in data:
            structure_training_data(line,dic)
        # for line in data:
        #     structure_training_data(line,dic)
        #     count +=1
        #     if count == 9: break
    f.close()

    # print(collective_dict)
    TRAIN_DATA = collective_dict['TRAINING_DATA']
    TRAIN_DATA_DOC = create_training_set(TRAIN_DATA)
    TRAIN_DATA_DOC.to_disk("./TEST_DATA.spacy")


if __name__ == '__main__':
    main()
