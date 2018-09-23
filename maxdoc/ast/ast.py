import abc
import enum
import json  # TODO: use yaml only?
import logging
import yaml

from .exceptions import ASTError


logger = logging.getLogger(__name__)


class ASTLoadError(ASTError):
    pass


@enum.unique
class NodeType(enum.Enum):
    DICT = '_ast_dict_'
    LIST = '_ast_list_'
    LITERAL = '_ast_literal_'
    TRANSFORMATION = '_ast_transformation_'


@enum.unique
class NodeField(enum.Enum):
    NODE_TYPE = '_ast_node_type_'
    PARENT = '_ast_parent_'
    CHILDREN = '_ast_children_'
    LITERAL_VALUE = '_ast_literal_value_'
    AST_TRANSFORMATION = '_ast_transformation_'


class Node(dict):
    def __init__(self, items=None, **kwargs):
        items = items or []
        items.update(kwargs)

        if NodeField.CHILDREN not in items:
            items[NodeField.CHILDREN] = []

        super().__init__(items)


    def _replace_child(self, old_child, new_child):
        idx = self[NodeField.CHILDREN].index(old_child)
        self[NodeField.CHILDREN].remove(old_child)
        self[NodeField.CHILDREN].insert(idx, new_child)

    def parents():
        p = self
        while True:
            p = p[NodeField.PARENT]
            if p is None:
                break
            yield p

    def __getattr__(self, k):
        if k == '__getstate__':
            return lambda : dict(self.__dict__)

        try:
            return self.__dict__[k]
        except KeyError as e:
            if k in self:
                return self[k]
            else:
                raise e

    def __setattr__(self, k, v):
        try:
            super().setattr(self, k, v)
        except AttributeError:
            self[k] = v

    @classmethod
    def from_ast_yaml(cls, yaml_node):
        if isinstance(yaml_node, (str, int, float, bool)):
            return yaml_node

        elif isinstance(yaml_node, list):
            return [ cls.from_ast_yaml(i) for i in yaml_node ]

        elif isinstance(yaml_node, dict):
            if NodeField.NODE_TYPE.name not in yaml_node:
                yaml_node[NodeField.NODE_TYPE.name] = NodeType.DICT

            return cls({
                cls._key_from_ast_yaml(k): cls.from_ast_yaml(v)
                for k, v in yaml_node.items()
            })

        else:
            raise ASTError("Don't know how to load AST Yaml value {!r}".format(yaml_node)) 

    @classmethod
    def _value_to_ast_yaml(cls, v):
        if isinstance(v, cls):
            return cls.to_ast_yaml(v)
        else:
            return yaml.dump(v)

    @classmethod
    def _key_to_ast_yaml(cls, k):
        if isinstance(k, str):
            return k
        return str(k.name)

    @classmethod
    def _key_from_ast_yaml(cls, k):
        if k == 'title':
            import pudb; pudb.set_trace()

        try:
            return NodeField.__members__[k]
        except KeyError:
            #print("Couldn't find {!r} in {!r}".format(k, NodeField.__members__))
            assert isinstance(k, str)
            return k

    @classmethod
    def to_ast_yaml(cls, ast_node):
        if isinstance(ast_node, list):
            return [cls.to_ast_yaml(i) for i in ast_node]

        elif isinstance(ast_node, Node):
            # treat other nodes as dictionaries to dump, with awareness of child
            # AST Nodes
            return {
                cls._key_to_ast_yaml(k): cls.to_ast_yaml(v)
                for k, v in ast_node.items() if k is not NodeField.PARENT
            }

        else:
            return cls._value_to_ast_yaml(ast_node)

    def __repr__(self):
        simplified_ast = self.__class__.to_ast_yaml(self)
        return json.dumps(simplified_ast, indent=4)


class ASTVisitor:
    def pre_visit(self, ast_node, parents, context):
        pass

    def post_visit(self, ast_node, parents, context):
        pass


class ASTParentPopulator(ASTVisitor):
    def pre_visit(self, ast_node, parents, context):
        ast_node[NodeField.PARENT] = parents[-1] if parents else None


class ASTWalker:
    def walk(self, ast_visitor, ast_node, parents=None, context=None, indent=1, dump_ast_walk=False):
        logger.debug("Visiting: {!r} (parents={!r})".format(
                     ast_node if not isinstance(ast_node, Node)
                     else ast_node.__dict__, parents)
        )

        assert isinstance(ast_node, Node)

        parents = parents or []
        context = context or {}

        ast_visitor.pre_visit(ast_node, parents, context)

        children = [c for c in ast_node[NodeField.CHILDREN]]
        for child in children:
            self.walk(ast_visitor, child, parents=parents + [ast_node],
                      context=context, indent=indent+1,
                      dump_ast_walk=dump_ast_walk)

        logger.debug(
            "Resuming:",
            ast_node if not isinstance(ast_node, Node)
                     else ast_node.__dict__
        )

        ast_visitor.post_visit(ast_node, parents, context)


def load_ast_yaml(fpath, top_level=True):
    with open(fpath) as fp:
        yaml_doc = yaml.load(fp.read())
        ast = Node.from_ast_yaml(yaml_doc)

    # make sure all non-root nodes have parents
    walker = ASTWalker()
    walker.walk(ASTParentPopulator(), ast)

    if top_level:
        # decorate document with transformation functions
        new_ast = Node({
            NodeField.NODE_TYPE: 'AST_TRANSFORM',
            NodeField.AST_TRANSFORMATION: 'compute_heading_levels',
            NodeField.CHILDREN: [ast],
        })
        ast[NodeField.PARENT] = new_ast
        ast = new_ast

    return ast
