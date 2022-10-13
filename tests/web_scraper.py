from boilerpy3 import extractors

extractor = extractors.ArticleExtractor()

# From a URL
content = extractor.get_content_from_url('https://www.westalabamaaging.org/benefits-services')
print(content)