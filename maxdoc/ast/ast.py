import abc
import yaml


class ASTLoadError(Exception):
    pass


class Node(metaclass=abc.ABCMeta):
    def __init__(self, **kwargs):
        if '_children' not in kwargs:
            kwargs['_children'] = []

        for k, v in kwargs.items():
            setattr(self, k, v)

    def _replace_child(self, old_child, new_child):
        self._children = [ new_child if c is old_child else c for c in self._children ]


def load_doc(fpath):
    with open(fpath) as fp:
        yaml_doc = yaml.load(fp.read())
        return load_yaml(yaml_doc)


def load_yaml(yaml_node):
    if isinstance(yaml_node, dict):
        if 'node_type' not in yaml_node:
            yaml_node['node_type'] = 'dict'
        return Node(**{ k: load_yaml(v) for k, v in yaml_node.items()})

    elif isinstance(yaml_node, list):
        return [ load_yaml(i) for i in yaml_node ]

    else:
        return yaml_node
