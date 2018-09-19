from ..exceptions import RenderError
from .base import BaseRenderer


class PDFRenderer(BaseRenderer):
    def render(self, item):
        raise RenderError("{} doesn't know how to render {!r}".format(item))
