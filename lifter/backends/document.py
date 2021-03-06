import contextlib

from .python import DummyStore
from six.moves.urllib.request import urlopen


class DocumentStore(DummyStore):
    """
    Return results from arbitrary static
    sources (HTTP, local file system, etc.)
    """
    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.parser = kwargs.pop('parser', None)
        self.encoding = kwargs.pop('encoding', 'utf-8')

        super(DocumentStore, self).__init__(*args, **kwargs)

    def get_document(self):
        return urlopen(self.url)

    def parse_document(self, document, model, adapter):
        if not self.parser:
            return self.from_lines(document, model, adapter)
        else:
            return self.from_parser(document, model, adapter)

    def from_parser(self, document, model, adapter):
        parsed = self.parser.parse(document.read().decode(self.encoding))
        return [adapter.parse(result, model) for result in parsed]

    def from_lines(self, document, model, adapter):
        return [
            adapter.parse(line.decode(self.encoding), model)
            for line in document
        ]

    def load(self, model, adapter):
        with contextlib.closing(self.get_document()) as document:
            return self.parse_document(document, model, adapter)
