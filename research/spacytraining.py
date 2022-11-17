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
                print("No pattern matches found. Keyword:", kw)

    # add any found entities into a JSON format within collective_dict
    if len(entities) > 0:
        results = [text, {"entities": entities}]
        collective_dict['TRAINING_DATA'].append(results)
        return


def main():
    # dic = {
    #     "ORG": ["Brent Senior Activity Center", "Woodstock Senior Activity Center"],
    #     "ADDRESS": ["10445 AL-5 Brent, AL 35034", "8515 Hwy. 5 Woodstock, AL 35188"],
    #     "PHONE": ["205-926-3968", "205-938-9790"],
    #     "PERSON": ["Wanda Holder", "Frankie Grammer"],
    #     "EMAIL": ["sacbrent@hotmail.com"],
    #     "HOURS": ["Monday - Friday  8:00 A.M. - 2:00 P.M.", "Monday - Friday 9:00 A.M. - 1:00 P.M."]
    # }
    dic = {
        # "LOC": ["Bibb co.", "Fayette Co.", "Greene Co.", "Hale Co.", "Lamar Co.", "Pickens Co.", "Tuscaloosa Co."],
        "LOC": ["Bibb co.", "Fayette Co.", "Greene Co."],
        "ORG": ["Bibb Co. Farmers Market", "Fayette Co. Farmers Market", "Greene Co. Farmers Market", "United Farmers Market"],
        "ADDRESS": ["268 Belcher St Centreville, AL 35042", "650 McConnell Loop Fayette, AL", "137 Furse Ave Eutaw, AL 35462", "Co Rd 18 & Co Rd 41 Forkland, AL"],
        "PHONE": ["334-518-9049", "205-596-3904", "205-372-9458", "205-799-5204", "334-289-4645"],
        "HOURS": ["Saturdays May - Oct. 8:00 A.M. - 12:00 P.M.", "June Tues. & Saturdays 7:00 A.M. - Until Thursdays 4:00 P.M. - 7:00 P.M.", "Saturdays April - Sept. 8:00 A.M. - 12:00 P.M.", "Saturdays May - Oct. 10:00 A.M. - 3:00 P.M."]
    }
    # text1 = "Brent Senior Activity Center 10445 AL-5 Brent, AL 35034 205-926-3968 Center Director:  Wanda Holder sacbrent@hotmail.com Open Monday - Friday  8:00 A.M. - 2:00 P.M."
    # text2 = "Woodstock Senior Activity Center 28515 Hwy. 5 Woodstock, AL 35188 205-938-9790 Center Director:  Frankie Grammer Open Monday - Friday 9:00 A.M. - 1:00 P.M."
    with open("Alabama_Senior_Farmers_Market_Nutrition_Program__FMNP____Area_Agency_on_Aging_of_West_Alabama.txt", "r") as f:
        text = f.read()
        structure_training_data(text,dic)
    f.close()
    # structure_training_data(text1, dic)
    # structure_training_data(text2, dic)

    print(collective_dict)


if __name__ == '__main__':
    main()
