import abc
import yaml


class ASTLoadError(Exception):
    pass


class Node(metaclass=abc.ABCMeta):
    def __init__(self, **kwargs):
        self._children = kwargs['_children'] if '_children' in kwargs else []

class DictNode(Node):
    pass

class TextNode(Node):
    def __init__(self, *, body=None, **kwargs):
        super().__init__(**kwargs)
        if body is None:
            body = ''
        self.body = body


class BookNode(Node):
    def __init__(self, *, id=None):
        super().__init__(**kwargs)
        self._id = id


ALL_AST_NODE_TYPES = { 'Text': TextNode, 'Book': BookNode }


def load_doc(fpath):
    with open(fpath) as fp:
        yaml_doc = yaml.load(fp.read())
        return load_yaml(yaml_doc)


def load_yaml(yaml_node):
    if isinstance(yaml_node, dict) and 'node_type' in yaml_node:
        node_type_name = yaml_node['node_type']
        node_type = ALL_AST_NODE_TYPES[node_type_name]
        loaded_items = { k: load_yaml(v) for k, v in yaml_node.items() }
        return node_type(**loaded_items)

    elif isinstance(yaml_node, list):
        return [ load_yaml(i) for i in yaml_node ]

    else:
        return yaml_node