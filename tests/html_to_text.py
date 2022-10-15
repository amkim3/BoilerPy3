from boilerpy3 import extractors


def html_to_text(html_file):
    extractor = extractors.KeepEverythingExtractor()

    with open("htmlExtractedText.txt", "a") as file:
        file.write(extractor.get_content_from_file(html_file))
    file.close()