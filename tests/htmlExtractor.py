from datetime import time

from boilerpy3 import extractors
import time

extractor = extractors.KeepEverythingExtractor()
# From a URL
with open("extractedText11.txt", "a") as file:
    file.write(extractor.get_content_from_file('beautifulsoupoutput.html'))
file.close()