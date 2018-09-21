from .exceptions import RenderError
from .base import Renderer

from .. import db
from .. import ast


class HTMLRenderer(Renderer):
    def _pre_render(self, config, db_session, ast_node):
        if hasattr(ast_node, 'node_type'):
            if ast_node.node_type == 'Document':
                    config.out_fp.write(("<html>\n"
                                         + "    <head>\n"
                                         + "        <title>{}</title>\n".format(ast_node.title)
                                         + "    </head>\n"
                                         + "    <body>\n"))
            elif ast_node.node_type == 'Para':
                    config.out_fp.write("        <p>")
            elif ast_node.node_type == 'Strong':
                    config.out_fp.write("<strong>")
            elif ast_node.node_type == 'Emph':
                    config.out_fp.write("<em>")
            elif ast_node.node_type == 'Sub':
                    config.out_fp.write("<sub>")
            elif ast_node.node_type == 'Sup':
                    config.out_fp.write("<sup>")
        else:
            super()._pre_render(config, db_session, ast_node)

    def _post_render(self, config, db_session, ast_node):
        if hasattr(ast_node, 'node_type'):
            if ast_node.node_type == 'Document':
                config.out_fp.write(("    </body>\n"
                                     "</html>"))
            elif ast_node.node_type == 'Para':
                config.out_fp.write("</p>\n")
            elif ast_node.node_type == 'Strong':
                    config.out_fp.write("</strong>")
            elif ast_node.node_type == 'Emph':
                    config.out_fp.write("</em>")
            elif ast_node.node_type == 'Sub':
                    config.out_fp.write("</sub>")
            elif ast_node.node_type == 'Sup':
                    config.out_fp.write("</sup>")
        else:
            super()._post_render(config, db_session, ast_node)

    def _render_body(self, config, db_session, ast_node):
        db_node = self._get_ast_db_node(config, db_session, ast_node)

        if isinstance(db_node, (list, dict)):
            super()._render_body(config, db_session, ast_node)

        elif isinstance(db_node, db.Book):
            if db_node.url is not None:
                config.out_fp.write("<a href='{}'>".format(db_node.url))

            config.out_fp.write("{}".format(db_node.title))

            if db_node.url is not None:
                config.out_fp.write("</a>")

        elif isinstance(db_node, db.Author):
            if db_node.url is not None:
                config.out_fp.write("<a href='{}'>".format(db_node.url))

            config.out_fp.write("<a href='{}'>{}</a>".format('mailto:' + db_node.id, db_node.pen_name))

            if db_node.url is not None:
                config.out_fp.write("</a>")

        elif hasattr(ast_node, 'node_type') and ast_node.node_type == 'Text':
            config.out_fp.write(ast_node.body)

        else:
            super()._render_body(config, db_session, ast_node)
