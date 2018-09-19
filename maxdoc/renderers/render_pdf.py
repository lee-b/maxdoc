from .exceptions import RenderError
from .base import Renderer


class PDFRenderer(Renderer):
    def render(self, config, db_session, ast_node):
        super().render(config, db_session, ast_node)
