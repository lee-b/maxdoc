import abc
import yaml
import json

from .exceptions import ASTError


class ASTLoadError(ASTError):
    pass


class Node(metaclass=abc.ABCMeta):
    def __init__(self, **kwargs):
        if '_children' not in kwargs:
            kwargs['_children'] = []

        for k, v in kwargs.items():
            setattr(self, k, v)

    def _replace_child(self, old_child, new_child):
        self._children = [ new_child if c is old_child else c for c in self._children ]


class ASTVisitor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def pre_visit(self, ast_node, parents, context):
        pass

    @abc.abstractmethod
    def post_visit(self, ast_node, parents, context):
        pass


class ASTWalker:
    def walk(self, ast_visitor, ast_node, parents=None, context=None, indent=1, dump_ast_walk=False):
        if dump_ast_walk:
            print(" " * 4 * indent + "Visiting: {!r} (parents={!r})".format(ast_node if not isinstance(ast_node, Node) else ast_node.__dict__, parents))

        if parents is None:
            parents = []

        if context is None:
            context = {}

        ast_visitor.pre_visit(ast_node, parents, context)

        children = []

        if isinstance(ast_node, Node) and hasattr(ast_node, '_children'):
            children = [c for c in ast_node._children]

        elif isinstance(ast_node, list):
            children = [c for c in ast_node]

        for child in children:
            self.walk(ast_visitor, child, parents=parents + [ast_node], context=context, indent=indent+1, dump_ast_walk=dump_ast_walk)

        if dump_ast_walk: 
            print(" " * 4 * indent + "Resuming:", ast_node if not isinstance(ast_node, Node) else ast_node.__dict__)

        ast_visitor.post_visit(ast_node, parents, context)


def load_ast_yaml(fpath, top_level=True):
    with open(fpath) as fp:
        yaml_doc = yaml.load(fp.read())
        ast = ast_from_yaml_node(yaml_doc)

    if top_level:
        # decorate document with transformation functions
        ast = Node(
            _transformation='compute_heading_levels',
            _children=[ast],
        )

    return ast

def ast_from_yaml_node(yaml_node):
    if isinstance(yaml_node, dict):
        if 'node_type' not in yaml_node:
            yaml_node['node_type'] = 'dict'

        return Node(**{ k: ast_from_yaml_node(v) for k, v in yaml_node.items()})

    elif isinstance(yaml_node, list):
        return [ ast_from_yaml_node(i) for i in yaml_node ]

    else:
        return yaml_node


def simplify_nodes(ast):
    if isinstance(ast, Node):
        ast = ast.__dict__

    if isinstance(ast, dict):
        return {k: simplify_nodes(v) for k, v in ast.items()}

    elif isinstance(ast, list):
        return [simplify_nodes(i) for i in ast]

    else:
        return ast

def dump_nodes(ast, indent=4):
    simplified_ast = simplify_nodes(ast)
    return json.dumps(simplified_ast, indent=indent)
