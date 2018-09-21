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


def load_ast_yaml(fpath):
    with open(fpath) as fp:
        yaml_doc = yaml.load(fp.read())
        return ast_from_yaml_node(yaml_doc)


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
