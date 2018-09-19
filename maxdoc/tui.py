from .config import get_config
from .db import init_db
from .gatherers import ALL_GATHERERS
from .renderers import ALL_RENDERERS
from .ast import load_doc, transform_ast


def gather_data(config, db_session):
    for gatherer in ALL_GATHERERS:
        gatherer.gather_data(config, db_session)


def main(args):
    config = get_config(args)

    db_engine, DBSession = init_db()
    db_session = DBSession()

    pipeline = {
        "Loading data": gather_data,
    }

    for stage, handler in pipeline.items():
        print("{}...".format(stage), end="")
        handler(config, db_session)
        print("")

    ast = load_doc(config.input_doc)

    transform_ast(config, db_session, ast, None)

    renderer = ALL_RENDERERS[config.renderer]
    renderer.render(config, db_session, ast)
