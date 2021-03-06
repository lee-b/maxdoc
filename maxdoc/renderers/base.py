import abc
import logging
import sys

import sqlalchemy

from .. import db
from .. import ast


logger = logging.getLogger(__name__)


class Renderer(metaclass=abc.ABCMeta):
    def _pre_render(self, config, db_session, ast_node):
        pass

    def _render_body(self, config, db_session, ast_node):
        pass

    def _post_render(self, config, db_session, ast_node):
        pass

    def _get_ast_db_node(self, config, db_session, ast_node):
        if isinstance(ast_node, list):
            return None

        try:
            db_type = getattr(db, ast_node[ast.NodeField.NODE_TYPE])
        except AttributeError:
            return None

        try:
            return db_session.query(db_type).filter_by(id=ast_node.id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            logger.error(
                "ERROR: No DB record found for {}(id={!r})".format(
                    ast_node[ast.NodeField.NODE_TYPE], ast_node['id']
                )
            )
            sys.exit(20)

    def render(self, config, db_session, ast_node):
        self._pre_render(config, db_session, ast_node)
        self._render_body(config, db_session, ast_node)

        if isinstance(ast_node, list):
            children = ast_node

        else:
            children = ast_node[ast.NodeField.CHILDREN]

        for ast_child_node in children:
            self.render(config, db_session, ast_child_node)

        self._post_render(config, db_session, ast_node)

    def __repr__(self):
        return self.__class__.__name__
