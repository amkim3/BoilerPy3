import os

import pytest

from boilerpy3.document import DefaultLabels, TextBlock
from boilerpy3.exceptions import HTMLExtractionError
from boilerpy3.extractors import ArticleExtractor, Extractor

TESTS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

extractor = Extractor(None)  # noqa
default_words = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec fermentum tincidunt magna, eu " \
                "pulvinar mauris dapibus pharetra. In varius, nisl a rutrum porta, sem sem semper lacus, et varius " \
                "urna tellus vel lorem. Nullam urna eros, luctus eget blandit ac, imperdiet feugiat ipsum. Donec " \
                "laoreet tristique mi a bibendum. Sed pretium bibendum scelerisque. Mauris id pellentesque turpis. " \
                "Mauris porta adipiscing massa, quis tempus dui pharetra ac. Morbi lacus mauris, feugiat ac tempor " \
                "ut, congue tincidunt risus. Pellentesque tincidunt adipiscing elit, in fringilla enim scelerisque " \
                "vel. Nulla facilisi. ".split(' ')


def _content_item(s):
    if isinstance(s, int):
        return ' '.join(default_words[:s])
    else:
        return s


def _make_content(str_arr):
    return [_content_item(s) for s in str_arr]


def _make_doc_2(template, content_arr):
    template_arr = template.split('*')
    s = ""
    for i, j in zip(template_arr[:-1], content_arr):
        s += i + j
    s += template_arr[-1]
    doc = extractor.parse_doc(s)
    return doc


def test_blocks():
    template = "<html><body><p>*</p><div>*<p>*</p>*</div></body></html>"
    content = _make_content([4, 5, 6, 7])
    doc = _make_doc_2(template, content)
    
    blocks = doc.text_blocks
    text_arr = [block.text for block in blocks]
    num_words = [block.num_words for block in blocks]
    assert text_arr == content
    assert num_words == [4, 5, 6, 7]


def test_anchor():
    template = "<html><body><p>*</p><div>*<a href='half.html'>*</a></div><a href='full.html'><p>*</p></a></body></html>"
    content = _make_content([6, "end with space ", 3, 6])
    doc = _make_doc_2(template, content)
    
    blocks = doc.text_blocks
    text_arr = [block.text for block in blocks]
    density_arr = [block.link_density for block in blocks]
    num_anchor_words = [block.num_words_in_anchor_text for block in blocks]
    assert text_arr == [content[0], content[1] + content[2], content[3]]
    assert num_anchor_words == [0, 3, 6]
    assert density_arr == [0.0, 0.5, 1.0]


def test_title():
    title_text = "THIS IS TITLE"
    s = "<html><head><title>" + title_text + "</title></head><body><p>THIS IS CONTENT</p></body></html>"
    doc = extractor.parse_doc(s)
    assert doc.title == title_text


def test_body():
    body_text = "THIS IS CONTENT"
    s = "<html><head><p>NOT IN BODY</p></head><body><p>" + body_text + "</p></body></html>"
    doc = extractor.parse_doc(s)
    text_arr = [block.text for block in doc.text_blocks]
    assert text_arr == [body_text]


def test_inline():
    template = "<html><body><div><h1>*</h1><h4>*</h4></div><div><span>*</span><b>*</b></div></body></html>"
    content = ['AA', 'BB', 'CC', 'DD']
    doc = _make_doc_2(template, content)
    
    blocks = doc.text_blocks
    text_arr = [block.text for block in blocks]
    assert text_arr == [content[0], content[1], content[2] + content[3]]


def test_ignorable():
    template = "<html><body><p>*</p><option><p>*</p></option></body></html>"
    content = _make_content([10, 12])
    doc = _make_doc_2(template, content)
    
    blocks = doc.text_blocks
    text_arr = [block.text for block in blocks]
    assert text_arr == [content[0]]


def assert_range(val, minval, maxval):
    assert minval <= val <= maxval


def test_textDensity():
    template = "<html><body><p>*</p><p>*</p></body></html>"
    content = _make_content([80, "one, !!! two"])
    doc = _make_doc_2(template, content)
    
    blocks = doc.text_blocks
    num_arr = [[block.num_words, block.num_words_in_wrapped_lines, block.num_wrapped_lines, block.text_density] for
               block in blocks]
    
    # exact values are unknown, approximate value range to check
    assert blocks[0].num_words == 80
    assert_range(blocks[0].num_words_in_wrapped_lines, 60, 80)
    assert_range(blocks[0].num_wrapped_lines, 4, 7)
    assert_range(blocks[0].text_density, 8, 16)
    
    assert num_arr[1] == [2, 2, 1, 2]


def test_block_idxs():
    template = "<html><body><p>*  </p>  <p> * </p><p>*  </p><p>*  </p></body></html>"
    content = _make_content([11, 12, 13, 14])
    doc = _make_doc_2(template, content)
    
    blocks = doc.text_blocks
    idx_arr = [[block.offset_blocks_start, block.offset_blocks_end] for block in blocks]
    assert idx_arr == [[0, 0], [1, 1], [2, 2], [3, 3]]


def test_tag_level():
    template = "<html><body><div><p><span><a href='x.html'>*</a></span></p>*</div></body></html>"
    content = _make_content([5, 6])
    doc = _make_doc_2(template, content)
    
    blocks = doc.text_blocks
    level_arr = [block.tag_level for block in blocks]
    assert level_arr == [5, 3]


def test_merge():
    block1 = TextBlock("AA BB CC ", {0}, 3, 3, 3, 1, 0)
    block2 = TextBlock("DD EE FF GG HH II JJ .", {1}, 6, 0, 6, 2, 1)
    block1.add_labels(DefaultLabels.MIGHT_BE_CONTENT)
    block2.add_labels(DefaultLabels.ARTICLE_METADATA)
    block1.merge_next(block2)
    assert block1.text == "AA BB CC \nDD EE FF GG HH II JJ ."
    assert block1.num_words == 9
    assert block1.num_words_in_anchor_text == 3
    assert round(abs(block1.link_density - 1.0 / 3.0), 7) == 0
    assert block1.text_density == 3
    assert block1.labels == {DefaultLabels.MIGHT_BE_CONTENT, DefaultLabels.ARTICLE_METADATA}
    assert block1.offset_blocks_start == 0
    assert block1.offset_blocks_end == 1


def test_extraction():
    expected_text = """
Learn Kubernetes Basics
Kubernetes (K8s) is an open-source system for
                automating deployment, scaling, and management of containerized applications.
It groups containers that make up an application into logical units for easy management and
                    discovery. Kubernetes builds upon 15 years of experience of running production
                        workloads at Google , combined with best-of-breed ideas and practices from the community.
Planet Scale
Designed on the same principles that allows Google to run billions of containers a week, Kubernetes
                    can scale without increasing your ops team.
Never Outgrow
Whether testing locally or running a global enterprise, Kubernetes flexibility grows with you to
                    deliver your applications consistently and easily no matter how complex your need is.
Run Anywhere
Kubernetes is open source giving you the freedom to take advantage of on-premises, hybrid, or public
                    cloud infrastructure, letting you effortlessly move workloads to where it matters to you.
The Challenges of Migrating 150+ Microservices to Kubernetes
By Sarah Wells, Technical Director for Operations and Reliability, Financial Times
Watch Video
    """
    expected_html = """<html><body class="page"><div></div><header><a href="/" class="logo"></a><div class="nav-buttons"><ul class="global-nav"><li><a href="/docs/"></a></li><li><a href="/blog/"></a></li><li><a href="/partners/"></a></li><li><a href="/community/"></a></li><li><a href="/case-studies/"></a></li><li><a href="#"><span class="ui-icon ui-icon-carat-1-s"></span></a><ul><li><a href="/zh/"></a></li><li><a href="/ko/"></a></li><li><a href="/ja/"></a></li><li><a href="/fr/"></a></li><li><a href="/de/"></a></li><li><a href="/es/"></a></li><li><a href="/pt/"></a></li><li><a href="/id/"></a></li></ul></li><li><a href="#"><span class="ui-icon ui-icon-carat-1-s"></span></a><ul><li><a href="https://kubernetes.io"></a></li><li><a href="https://v1-14.docs.kubernetes.io"></a></li><li><a href="https://v1-13.docs.kubernetes.io"></a></li><li><a href="https://v1-12.docs.kubernetes.io"></a></li><li><a href="https://v1-11.docs.kubernetes.io"></a></li></ul></li></ul><a href="/docs/tutorials/kubernetes-basics/" class="button"></a><button><div></div></button></div><nav><main><div class="nav-box"><h3><a href="/docs/tutorials/hello-minikube/"></a></h3><p></p></div><div class="nav-box"><h3><a href="/docs/home/"></a></h3><p><a href="/editdocs/"></a></p></div><div class="nav-box"><h3><a href="/blog/"></a></h3><p></p></div></main><main><div class="left"><h5 class="github-invite"></h5><a href="https://github.com/kubernetes/kubernetes" class="button"></a></div><div class="right"><h5 class="github-invite"></h5><div class="social"><a href="https://twitter.com/kubernetesio" class="twitter"><span></span></a><a href="https://github.com/kubernetes/kubernetes" class="github"><span></span></a><a href="http://slack.k8s.io/" class="slack"><span></span></a><a href="https://stackoverflow.com/questions/tagged/kubernetes" class="stack-overflow"><span></span></a><a href="https://discuss.kubernetes.io" class="mailing-list"><span></span></a><a href="https://calendar.google.com/calendar/embed?src=nt2tcnbtbied3l6gi2h29slvc0%40group.calendar.google.com" class="calendar"><span></span></a></div></div><div class="clear"></div></main></nav></header><section class="light-text"><main><div><h1></h1><h5></h5></div><a x-boilerpipe-marker href="/docs/tutorials/kubernetes-basics/" class="button">Learn Kubernetes Basics</a></main></section><article class="page-content"><section><main><div class="image-wrapper"><img src="https://d33wubrfki0l68.cloudfront.net/1567471e7c58dc9b7d9c65dcd54e60cbf5870daa/da576/_common-resources/images/flower.png"></div><div class="content"><h3><a x-boilerpipe-marker href="/docs/concepts/overview/what-is-kubernetes/">Kubernetes (K8s)</a> is an open-source system for
                automating deployment, scaling, and management of containerized applications.</h3><p x-boilerpipe-marker>It groups containers that make up an application into logical units for easy management and
                    discovery. Kubernetes builds upon <a x-boilerpipe-marker href="http://queue.acm.org/detail.cfm?id=2898444">15 years of experience of running production
                        workloads at Google</a>, combined with best-of-breed ideas and practices from the community.</p></div></main><main><div class="image-wrapper"><img src="https://d33wubrfki0l68.cloudfront.net/33a12d8be0bc50be4738443101616e968c7afb8f/2c641/_common-resources/images/scalable.png"></div><div x-boilerpipe-marker class="content"><h4 x-boilerpipe-marker>Planet Scale</h4><p x-boilerpipe-marker>Designed on the same principles that allows Google to run billions of containers a week, Kubernetes
                    can scale without increasing your ops team.</p></div></main><main><div class="image-wrapper"><img src="https://d33wubrfki0l68.cloudfront.net/dbc75a944a909b2d52bf24ad06d485eca12af892/4fb42/_common-resources/images/blocks.png"></div><div x-boilerpipe-marker class="content"><h4 x-boilerpipe-marker>Never Outgrow</h4><p x-boilerpipe-marker>Whether testing locally or running a global enterprise, Kubernetes flexibility grows with you to
                    deliver your applications consistently and easily no matter how complex your need is.</p></div></main><main><div class="image-wrapper"><img src="https://d33wubrfki0l68.cloudfront.net/bc2e475ac5fee0199eb3f4a0879cd559e8929f3a/4a628/_common-resources/images/suitcase.png"></div><div x-boilerpipe-marker class="content"><h4 x-boilerpipe-marker>Run Anywhere</h4><p x-boilerpipe-marker>Kubernetes is open source giving you the freedom to take advantage of on-premises, hybrid, or public
                    cloud infrastructure, letting you effortlessly move workloads to where it matters to you.</p></div></main></section><section><div x-boilerpipe-marker class="light-text"><h2 x-boilerpipe-marker>The Challenges of Migrating 150+ Microservices to Kubernetes</h2><p x-boilerpipe-marker>By Sarah Wells, Technical Director for Operations and Reliability, Financial Times</p><button x-boilerpipe-marker>Watch Video</button><br><br><br><a href="https://events.linuxfoundation.org/events/kubecon-cloudnativecon-north-america-2019"></a><br><br><br><br><a href="https://events.linuxfoundation.org/events/kubecon-cloudnativecon-europe-2020/"></a></div><div><iframe></iframe><button></button></div></section><section><main><h3 class="center"></h3><div class="feature-box"><div><h4><a href="/docs/concepts/services-networking/service/"></a></h4></div><div><h4><a href="/docs/concepts/configuration/manage-compute-resources-container/"></a></h4></div></div><div class="feature-box"><div><h4><a href="/docs/concepts/storage/persistent-volumes/"></a></h4><a href="https://cloud.google.com/storage/"></a><a href="https://aws.amazon.com/products/storage/"></a></div><div><h4><a href="/docs/concepts/workloads/controllers/replicationcontroller/#how-a-replicationcontroller-works"></a></h4></div></div><div class="feature-box"><div><h4><a href="/docs/concepts/workloads/controllers/deployment/"></a></h4></div><div><h4><a href="/docs/concepts/configuration/secret/"></a></h4></div></div><div class="feature-box"><div><h4><a href="/docs/concepts/workloads/controllers/jobs-run-to-completion/"></a></h4></div><div><h4><a href="/docs/tasks/run-application/horizontal-pod-autoscale/"></a></h4></div></main></section><section><main><h3></h3><div><div><img src="https://d33wubrfki0l68.cloudfront.net/3a8cc4aa42f7b9bf14ee889c7fc800d51ad81281/7b98e/case-studies/chinaunicom/chinaunicom_featured_logo.png"><p></p><a href="/case-studies/chinaunicom/"></a></div><div><img src="https://d33wubrfki0l68.cloudfront.net/bece62971ff2d9abf68b824c752275653e672a4c/34b9e/case-studies/spotify/spotify_featured_logo.png"><p></p><a href="/case-studies/spotify/"></a></div><div><img src="https://d33wubrfki0l68.cloudfront.net/5d0175f0503d093decbbbf90dd45b8c35b8eace0/e2342/case-studies/nav/nav_featured_logo.png"><p></p><a href="/case-studies/nav/"></a></div><div><img src="https://d33wubrfki0l68.cloudfront.net/25a46b88d3bb29c8ab8e4e0a819344e7978a1996/4461a/case-studies/appdirect/appdirect_featured_logo.png"><p></p><a href="/case-studies/appdirect/"></a></div></div><h5><a href="/case-studies/"></a></h5></main></section><section><main><center><p><a href="https://cncf.io/"></a></p></center></main></section><section><main><link href="https://cdn-images.mailchimp.com/embedcode/horizontal-slim-10_7.css"><br><br><div><h5><a href="https://us10.campaign-archive.com/home/?u=3885586f8f1175194017967d6&amp;id=11c1b8bcb2"></a></h5></div><br><br></main></section></article><footer><main class="light-text"><nav><a href="/docs/home/"></a><a href="/blog/"></a><a href="/partners/"></a><a href="/community/"></a><a href="/case-studies/"></a></nav><div class="social"><div><a href="https://twitter.com/kubernetesio" class="twitter"><span></span></a><a href="https://github.com/kubernetes/kubernetes" class="github"><span></span></a><a href="http://slack.k8s.io/" class="slack"><span></span></a></div><div><a href="http://stackoverflow.com/questions/tagged/kubernetes" class="stack-overflow"><span></span></a><a href="https://discuss.kubernetes.io" class="mailing-list"><span></span></a><a href="https://calendar.google.com/calendar/embed?src=nt2tcnbtbied3l6gi2h29slvc0%40group.calendar.google.com" class="calendar"><span></span></a></div><div><a href="https://git.k8s.io/community/contributors/guide" class="button"></a></div></div><div class="center"><a href="https://git.k8s.io/website/LICENSE" class="light-text"></a></a></div><div class="center"><a href="https://www.linuxfoundation.org/trademark-usage" class="light-text"></a></div><div class="center"></div></main></footer><button class="flyout-button"></button></body></html>"""
    
    with open(os.path.join(TESTS_DIR, 'test.html')) as html_file:
        html = html_file.read()
    article_extractor = ArticleExtractor()
    extracted_text = article_extractor.get_content(html)
    assert expected_text.strip() == extracted_text.strip()
    
    extracted_html = article_extractor.get_marked_html(html)
    assert expected_html.strip() == extracted_html.strip()
    
    with open(os.path.join(TESTS_DIR, 'test_bad.html')) as html_file:
        html = html_file.read()
    with pytest.raises(HTMLExtractionError):
        article_extractor.get_content(html)
    
    article_extractor.raise_on_failure = False
    assert article_extractor.get_content(html)
