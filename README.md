# Fall 2022 Dementia Chatbot Research

![build](https://github.com/jmriebold/BoilerPy3/workflows/Tests/badge.svg)


## About

FarmersMarketTraining.py is the file to create training and test models to use with spacy.

NER_model_testing is used to test unseen data and see results

webscraper.py is used to extract text from webpages.

## Usage


## Extract webpage text
to run:
```shell
python webscraper.py https://www.westalabamaaging.org/alabama-farmers-market-program
```
**Note**: currently, a link is hardcoded in the code in line 76 for debugging.

## Train model

Run FarmersMarketTraining for train/test data by specifying which file in line 99, 113.
Initialize and train:
```shell
python -m spacy init fill-config base_config.cfg config.cfg
python -m spacy train config.cfg  --output ./output 
```

## Results
Run NER model to see visualization of results.
