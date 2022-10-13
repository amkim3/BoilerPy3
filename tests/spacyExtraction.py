import spacy
# from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')

# read in file
input_file = open('extractedText7.txt').read()
text = nlp(input_file)

# print(text.ents)
# extract sentences
# sentences = list(text.sents)
# print(sentences[1])
#
# for token in text:
#     print(token.text)

# for token in text:
#     print(token.text,'--',token.is_stop,'---',token.is_punct)

text_clean = [token for token in text if not token.is_stop and not token.is_punct]
#
for token in text_clean:
    print(token.text)


