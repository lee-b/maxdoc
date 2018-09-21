import abc
import os

from .ast import Node, load_ast_yaml


class ASTError(Exception):
    pass


class ASTTransform(metaclass=abc.ABCMeta):
    def execute(self, config, db_session, ast_node, child_handler, parent=None):
        """
        child_handler: similar function to call for child nodes, but which can determine
        the appropriate handler to call
        returns: (bool) whether to rescan the (sub)tree if parent is not None, else None
        """

        rescan = None

        while rescan in (None, True):
            rescan = self._pre_execute(config, db_session, ast_node, child_handler, parent=parent)
            rescan |= self._execute(config, db_session, ast_node, child_handler, parent=parent)

            if hasattr(ast_node, '_children') and ast_node._children:
                children_copy = list(ast_node._children)
                for child_node in children_copy:
                    rescan |= child_handler(config, db_session, child_node, child_handler, parent=ast_node)

            rescan |= self._post_execute(config, db_session, ast_node, child_handler, parent=parent)

            if parent is not None:
                return rescan

        return rescan

    def _pre_execute(self, config, db_session, ast_node, child_handler, parent=None):
        return False

    def _execute(self, config, db_session, ast_node, child_handler, parent=None):
        return False

    def _post_execute(self, config, db_session, ast_node, child_handler, parent=None):
        return False


class EnvVarASTTransform(ASTTransform):
    def _execute(self, config, db_session, ast_node, child_handler, parent=None):
        new_node = Node(node_type='Text', body=os.environ[ast_node.body])
        parent._replace_child(ast_node, new_node)
        return False


class ASTIncludeASTTransform(ASTTransform):
    def _execute(self, config, db_session, ast_node, child_handler, parent=None):
        new_node = load_ast_yaml(ast_node.path)
        parent._replace_child(ast_node, new_node)
        return False  # TODO: change to true, make sure rescanning included files and modifying parent ASTs works correctly


BUILTIN_AST_TRANSFORMS = {
    'env_var': EnvVarASTTransform(),
    'include_ast': ASTIncludeASTTransform(),
}


def transform_ast(config, db_session, ast_node, child_handler, parent=None):
    """
    Args:
        child_handler: Set this to None when calling from user code
    """
    class ASTNoOp(ASTTransform):
        pass

    no_op = ASTNoOp()

    if hasattr(ast_node, '_transformation') and ast_node._transformation is not None:
        try:
            handler = BUILTIN_AST_TRANSFORMS[ast_node._transformation]
        except KeyError as e:
            raise ASTError("Unknown AST transformation: {}".format(str(e))) from e

    else:
        handler = no_op

    rescan = None
    while rescan in (None, True):
        rescan = handler.execute(config, db_session, ast_node, transform_ast, parent=parent)

    return rescan if parent is not None else None
