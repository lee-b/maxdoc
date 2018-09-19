from .exceptions import RenderError
from .base import Renderer

from .. import db
from .. import ast


class HTMLRenderer(Renderer):
    def render(self, config, db_session, ast_node):
        db_node = self._get_ast_db_node(config, db_session, ast_node)

        if isinstance(db_node, db.Book):
            print("{}, by {}".format(item.title, item.author))

        elif isinstance(ast_node, ast.TextNode):
            print(ast_node.body, end="")

        else:
            super().render(config, db_session, ast_node)
