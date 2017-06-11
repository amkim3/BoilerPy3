
from .parser import BoilerpipeHTMLParser
from xml.sax.xmlreader import AttributesImpl
import cgi


def xmlEncode(s):
    return cgi.escape(s, quote=True)


class AnotherBoilerPipeHTMLParser(BoilerpipeHTMLParser):
    def error(self, message):
        pass

    def __init__(self):
        super(AnotherBoilerPipeHTMLParser, self).__init__()

    def handle_starttag(self, tag, attributes):
        self.startElement(tag, AttributesImpl(dict(attributes)))


class HTMLBoilerpipeMarker(object):

    def __init__(self, remove_elements=None, allowed_attributes=None):
        """ generated source for method __init__ """
        self.TA_IGNORABLE_ELEMENTS = remove_elements or self.TA_IGNORABLE_ELEMENTS
        self.ALLOWED_ATTRIBUTES = allowed_attributes or self.ALLOWED_ATTRIBUTES

    def process(self, doc, is_):
        """ generated source for method process_0 """
        implementation = Implementation(self)
        implementation.process(doc, is_)
        return implementation.html

    ALLOWED_ATTRIBUTES = ['class', 'href', 'src']
    TA_IGNORABLE_ELEMENTS = ['STYLE', 'SCRIPT', 'OPTION', 'NOSCRIPT', 'OBJECT', 'EMBED', 'APPLET', 'LINK', 'HEAD',
                             'SVG', 'SELECT', 'FORM']

    VOID_ELEMENTS = (
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta', 'param', 'source',
        'track', 'wbr'
    )


class Implementation(AnotherBoilerPipeHTMLParser):  # XMLReader
    """ generated source for class Implementation """
    html = ""
    inIgnorableElement = 0
    characterElementIdx = 0
    contentBitSet = set()

    def __init__(self, hl):
        """ generated source for method __init__ """

        self.hl = hl
        super(Implementation, self).__init__()

    def process(self, doc, is_):
        """ generated source for method process """
        for block in doc.getTextBlocks():
            if block.isContent():
                bs = block.getContainedTextElements()
                if bs:
                    self.contentBitSet = self.contentBitSet.union(bs)

        self.feed(is_)

    def endDocument(self):
        """ generated source for method endDocument """
        pass

    def startDocument(self):
        """ generated source for method startDocument """
        pass

    def startElement(self, qName, atts):
        """ generated source for method startElement """
        if qName.upper() in self.hl.TA_IGNORABLE_ELEMENTS:
            if qName.lower() not in self.hl.VOID_ELEMENTS:
                self.inIgnorableElement += 1

        if self.inIgnorableElement == 0:
            self.html += '<' + qName

            if self.characterElementIdx + 1 in self.contentBitSet:
                self.html += ' x-boilerpipe-marker'

            for attr_name, attr_value in atts.items():
                if attr_name not in self.hl.ALLOWED_ATTRIBUTES:
                    continue
                self.html += ' {0}=\"{1}\"'.format(attr_name, xmlEncode(attr_value or ""))

            self.html += '>'

    def endElement(self, qName):
        """ generated source for method endElement """
        try:
            if self.inIgnorableElement == 0:
                self.html += "</%s>" % qName
        finally:
            if qName.upper() in self.hl.TA_IGNORABLE_ELEMENTS:
                self.inIgnorableElement -= 1

    def characters(self, ch):
        """ generated source for method characters """
        self.characterElementIdx += 1
        if self.inIgnorableElement == 0:
            if self.characterElementIdx not in self.contentBitSet:
                return

            self.html += xmlEncode(str(ch))
