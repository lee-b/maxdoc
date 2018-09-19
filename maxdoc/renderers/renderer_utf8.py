from ..exceptions import RenderError
from .base import BaseRenderer


class UTF8Renderer(BaseRenderer):
    def render(self, item):
        raise RenderError("{} doesn't know how to render {!r}".format(item))
