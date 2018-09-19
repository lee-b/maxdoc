import inspect
import os
import sqlalchemy

from .. import db
from .generic import GenericConfigFileDataGatherer


def _generate_gatherers():
    def as_config_fname(cls):
        lowered = cls.__name__.lower()
        if lowered.endswith("y"):
            return lowered[:-1] + 'ies'
        else:
            return lowered + 's'

    items = [getattr(db, i) for i in dir(db)]

    for item in items:
        if inspect.isclass(item) and issubclass(item, db.Base) and item.__name__ != 'Base':
            fpath = os.path.join('data', as_config_fname(item)) + '.yaml'
            gatherer = GenericConfigFileDataGatherer(item, fpath)

            print(gatherer)
            yield gatherer


ALL_GATHERERS = list(_generate_gatherers())
