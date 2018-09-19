from ..exceptions import RenderError
from .base import BaseRenderer

from ..db import db


class HTMLRenderer(BaseRenderer):
    def render(self, item):
        if isinstance(item, db.Book):
            print("{}, by {}".format(item.title, item.author))

        else:
            raise RenderError("{} doesn't know how to render {!r}".format(item))
