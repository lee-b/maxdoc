import logging
import os

import jinja2

from .exceptions import RenderError
from .base import Renderer
from .. import db
from .. import ast


class Jinja2HTMLRenderer(Renderer):
    def __init__(self, template_paths=['templates/html/jinja2'], **kwargs):
        super().__init__(**kwargs)
        self._template_paths = template_paths
        self._loader = jinja2.FileSystemLoader([os.path.abspath(p) for p in self._template_paths])
        self._env = jinja2.Environment(loader=self._loader)

    def _load_template(self, basename, suffix):
        try:
            return self._env.get_template("{}_{}.html.jinja2".format(basename, suffix))
        except jinja2.exceptions.TemplateNotFound:
            return None
        except jinja2.exceptions.TemplateSyntaxError as e:
            raise RenderError("Template {}_{}: {}", basename, suffix, str(e)) from e

    def _render_template(self, config, db_session, ast_node, suffix):
        if hasattr(ast_node, 'node_type'):
            db_node = self._get_ast_db_node(config, db_session, ast_node)

            template = self._load_template(ast_node.node_type, suffix)
            if template is None:
                return False

            output = template.render(config=config, ast_node=ast_node, db_node=db_node)

            config.out_fp.write(output)

            return True

    def _pre_render(self, config, db_session, ast_node):
        if not self._render_template(config, db_session, ast_node, "pre"):
            super()._pre_render(config, db_session, ast_node)

    def _post_render(self, config, db_session, ast_node):
        if not self._render_template(config, db_session, ast_node, "post"):
            super()._post_render(config, db_session, ast_node)

    def _render_body(self, config, db_session, ast_node):
        if not self._render_template(config, db_session, ast_node, "body"):
            super()._render_body(config, db_session, ast_node)
