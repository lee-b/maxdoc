import abc
import os

from .ast import Node, NodeField, NodeType, load_ast_yaml, ASTWalker, ASTVisitor


class ASTError(Exception):
    pass


class ASTTransform(metaclass=abc.ABCMeta):
    def execute(self, config, db_session, ast_node, child_handler, parent=None):
        """
        child_handler: Similar function to call for child nodes, but which can
                       determine the appropriate handler to call.

        Returns:
            (bool) Whether to rescan the (sub)tree if parent is not None, else
            None
        """

        while True:
            rescan, ast_node = self._pre_execute(
                config, db_session, ast_node, child_handler, parent=parent
            )
            if rescan:
                return rescan, ast_node

            rescan, ast_node = self._execute(
                config, db_session, ast_node, child_handler, parent=parent
            )
            if rescan:
                return rescan, ast_node

            if isinstance(ast_node, Node) and ast_node[NodeField.CHILDREN]:
                children_copy = list(ast_node[NodeField.CHILDREN])

                for child_node in children_copy:
                    rescan, child_node = child_handler(
                        config, db_session, child_node, child_handler,
                        parent=ast_node
                    )
                    if rescan:
                        return rescan, ast_node

            rescan, ast_node = self._post_execute(
                config, db_session, ast_node, child_handler, parent=parent
            )
            if (parent is not None and rescan) or not rescan:
                break

        return False, ast_node

    def _pre_execute(self, config, db_session, ast_node, child_handler,
                     parent=None
    ):
        return False, ast_node

    def _execute(self, config, db_session, ast_node, child_handler, parent=None
    ):
        return False, ast_node

    def _post_execute(self, config, db_session, ast_node, child_handler,
                      parent=None
    ):
        return False, ast_node


class EnvVarASTTransform(ASTTransform):
    def _execute(self, config, db_session, ast_node, child_handler, parent=None
    ):
        new_node = Node(node_type='Text', body=os.environ[ast_node.body])
        parent._replace_child(ast_node, new_node)
        return False, new_node


class ASTIncludeASTTransform(ASTTransform):
    def _execute(self, config, db_session, ast_node, child_handler, parent=None
    ):
        new_node = load_ast_yaml(ast_node.path, top_level=False)
        parent._replace_child(ast_node, new_node)
        return True, new_node


class ASTHeadingLevelAdjuster(ASTVisitor):
    def pre_visit(self, ast_node, parents, context):
        if 'heading_level' not in context:
            context['heading_level'] = 0

        if hasattr(ast_node, 'node_type') and ast_node[NodeField.NODE_TYPE] == 'Head':
            context['heading_level'] += 1
            ast_node['_ast_heading_level_'] = context['heading_level']

    def post_visit(self, ast_node, parents, context):
        if isinstance(ast_node, Node) and ast_node[NodeField.NODE_TYPE] == 'Head':
            context['heading_level'] -= 1


class ASTHeadingLevelPruner(ASTVisitor):
    def __init__(self, max_level=None):
        assert max_level is not None
        self._max_level = max_level
        self._pruning = False
        self._relative_depth = [0]

    def pre_visit(self, ast_node, parents, context):
        if 'current_depth' not in context:
            context['current_depth'] = 0

        context['current_depth'] += 1

        if isinstance(ast_node, list):
            return

        else:
            assert isinstance(ast_node, Node)

            if 'current_level' not in context:
                context['current_level'] = 0

            if '_ast_heading_level_' in ast_node:
                context['current_level'] = ast_node['_ast_heading_level_']

            if (ast_node[NodeField.NODE_TYPE] == NodeType.AST_TRANSFORMATION
                and ast_node[NodeField.TRANSFORMATION] == 'prune_heading_levels'
            ):
                self._relative_depth.append(context['current_depth'])

            relative_prune_depth = self._max_level + self._relative_depth[-1]
            if (
                not self._pruning
                and context['current_level'] > relative_prune_depth
            ):
                self._pruning = True

    def post_visit(self, ast_node, parents, context):
        context['current_depth'] -= 1

        if isinstance(ast_node, Node) and '_ast_heading_level_' in ast_node:
            context['current_level'] = ast_node['_ast_heading_level_']

        if self._pruning:
            relative_prune_depth = self._max_level + self._relative_depth[-1]

            if context['current_level'] <= relative_prune_depth:
               self._pruning = False

            else:
               if not parents:
                   #raise ASTError(("INTERNAL ERROR: no parents for {!r} when"
                   #                "pruning!").format(ast_node)) # TODO
                   return

               parent = parents[-1]

               if isinstance(parent, Node):
                   parent[NodeField.CHILDREN].remove(ast_node)

               elif isinstance(parent, dict):
                   parent[NodeField.CHILDREN].remove(ast_node)

               elif isinstance(parent, list):
                   list.remove(ast_node)

        if (
            hasattr(ast_node, '_transformation')
            and ast_node._transformation == 'prune_heading_levels'
        ):
            self._relative_depth.pop()


class ComputeHeadingLevelsASTTransform(ASTTransform):
    def _execute(self, config, db_session, ast_node, child_handler, parent=None
    ):
        walker = ASTWalker()
        visitor = ASTHeadingLevelAdjuster()
        walker.walk(visitor, ast_node, dump_ast_walk=config.dump_ast_walk)
        return False, ast_node


class PruneHeadingLevelsASTTransform(ASTTransform):
    def _execute(self, config, db_session, ast_node, child_handler, parent=None
    ):
        walker = ASTWalker()
        visitor = ASTHeadingLevelPruner(max_level=ast_node.max_level)
        walker.walk(visitor, ast_node, dump_ast_walk=config.dump_ast_walk)
        return False, ast_node


BUILTIN_AST_TRANSFORMS = {
    'env_var': EnvVarASTTransform(),
    'include_ast': ASTIncludeASTTransform(),
    'compute_heading_levels': ComputeHeadingLevelsASTTransform(),
    'prune_heading_levels': PruneHeadingLevelsASTTransform(),
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
        if (
            isinstance(ast_node, Node) and ast_node[NodeField.NODE_TYPE] == NodeType.TRANSFORMATION
        ):
            try:
                handler = BUILTIN_AST_TRANSFORMS[ast_node[NodeField.AST_TRANSFORMATION]]
            except KeyError as e:
                raise ASTError(
                    "Unknown AST transformation: {}".format(str(e))
                ) from e

        else:
            handler = no_op

        rescan, ast_node = handler.execute(
            config, db_session, ast_node, transform_ast, parent=parent
        )

        if (parent is not None and rescan) or not rescan:
            break

    return rescan, ast_node
