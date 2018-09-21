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

        while True:
            rescan, ast_node = self._pre_execute(config, db_session, ast_node, child_handler, parent=parent)
            if rescan:
                return rescan, ast_node

            rescan, ast_node = self._execute(config, db_session, ast_node, child_handler, parent=parent)
            if rescan:
                return rescan, ast_node

            if hasattr(ast_node, '_children') and ast_node._children:
                children_copy = list(ast_node._children)
                for child_node in children_copy:
                    rescan, child_node = child_handler(config, db_session, child_node, child_handler, parent=ast_node)
                    if rescan:
                        return rescan, ast_node

            rescan, ast_node = self._post_execute(config, db_session, ast_node, child_handler, parent=parent)
            if not rescan:
                break 

        return rescan, ast_node

    def _pre_execute(self, config, db_session, ast_node, child_handler, parent=None):
        return False, ast_node

    def _execute(self, config, db_session, ast_node, child_handler, parent=None):
        return False, ast_node

    def _post_execute(self, config, db_session, ast_node, child_handler, parent=None):
        return False, ast_node


class EnvVarASTTransform(ASTTransform):
    def _execute(self, config, db_session, ast_node, child_handler, parent=None):
        new_node = Node(node_type='Text', body=os.environ[ast_node.body])
        parent._replace_child(ast_node, new_node)
        return False, new_node


class ASTIncludeASTTransform(ASTTransform):
    def _execute(self, config, db_session, ast_node, child_handler, parent=None):
        import pudb; pudb.set_trace()
        new_node = load_ast_yaml(ast_node.path)
        parent._replace_child(ast_node, new_node)
        return True, new_node


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

    rescan = None
    while True:
        if hasattr(ast_node, '_transformation') and ast_node._transformation is not None:
            try:
                handler = BUILTIN_AST_TRANSFORMS[ast_node._transformation]
            except KeyError as e:
                raise ASTError("Unknown AST transformation: {}".format(str(e))) from e

        else:
            handler = no_op

        rescan, ast_node = handler.execute(config, db_session, ast_node, transform_ast, parent=parent)

        if not rescan:
            break

    return rescan if parent is not None else None, ast_node
