import spacy


# load the trained model
from spacy import displacy

nlp_output = spacy.load("output/model-best")
output = open("results.txt", "w")

def model_visualization(text):
    # pass our test instance into the trained pipeline
    doc = nlp_output(text)

    # customize the label colors
    colors = {"SERVICE": "linear-gradient(90deg, #E1D436, #F59710)"}
    options = {"ents": ["SERVICE"], "colors": colors}

    # visualize the identified entities
    # displacy.render(doc, style="ent",
    #                 options=options,
    #                 minify=True,
    #                 jupyter=True)
    # displacy.serve(doc, style='ent')

    # print out the identified entities
    print("\nIDENTIFIED ENTITIES:")
    [output.write(ent.text + '\n') for ent in doc.ents]
    output.write('\n')
    [print(ent.text) for ent in doc.ents]
    return


def main():
    with open("validation.txt", "r") as f:
        data = f.read().splitlines()
        for line in data:
            model_visualization(line)
    f.close()


if __name__ == '__main__':
    main()