from collections import namedtuple

from django.http import HttpResponse


class AttachmentHttpResponse(HttpResponse):
    def __init__(self, content, name):
        super().__init__(content=content)
        self.setdefault("Content-Disposition", f'attachment; filename="{name}"')


PseudoResponse = namedtuple("PseudoResponse", ["content", "status_code"])
