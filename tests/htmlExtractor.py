from datetime import time

from boilerpy3 import extractors
import time

extractor = extractors.KeepEverythingExtractor()
# From a URL
with open("htmlextractedtext.txt", "a") as file:
    file.write(extractor.get_content_from_file('beautifulsoupoutput1.html'))
file.close()