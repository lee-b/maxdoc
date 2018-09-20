import abc
from .. import db
from .. import ast


class Renderer(metaclass=abc.ABCMeta):
    def _pre_render(self, config, db_session, ast_node):
        pass

    def _render_body(self, config, db_session, ast_node):
        pass

    def _post_render(self, config, db_session, ast_node):
        pass

    def _get_ast_db_node(self, config, db_session, ast_node):
        try:
            db_type = getattr(db, ast_node.__class__.__name__[:-len('Node')])
        except AttributeError:
            return None

        return db_session.query(db_type).filter_by(id=ast_node.id).one()

    def render(self, config, db_session, ast_node):
        self._pre_render(config, db_session, ast_node)
        self._render_body(config, db_session, ast_node)

        if isinstance(ast_node, ast.Node):
            for ast_child_node in ast_node._children:
                self.render(config, db_session, ast_child_node)

        self._post_render(config, db_session, ast_node)

    def __repr__(self):
        return self.__class__.__name__
