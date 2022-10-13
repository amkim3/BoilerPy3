from datetime import time

from boilerpy3 import extractors
import time

extractor = extractors.ArticleExtractor()
count = 1
# From a URL
with open("extractedText6.txt", "a") as file:
    with open("updatedLinks.txt") as urls:
        for url in urls:
            extracted = None
            file.write(url + '\n')
            for x in range(0,4):
                try:
                    file.write(extractor.get_content_from_url(url))
                    print(url)
                    error = None
                except Exception as e:
                    error = str(e)
                if error:
                    time.sleep(5)
                else:
                    break
urls.close()
file.close()