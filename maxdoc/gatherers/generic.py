import logging
import os
import sys
import yaml

from ..db import *
from ..data import DataGatherer


logger = logging.getLogger(__name__)


class GenericConfigFileDataGatherer(DataGatherer):
    """A quick, hacky way to load yaml files directly into the DB.
    
    WARNING: This has NO real user input sanitisation!!!  It should
             NOT be used with untrusted data.
    """

    def __init__(self, data_type, fpath):
        self._data_type = data_type
        self._fpath = fpath

    def gather_data(self, config, db_session):
        if os.path.exists(self._fpath):
            logger.info(
                "Gathering {} data from {}...".format(
                    self._data_type.__name__, self._fpath
                ),
                end=""
            )
            sys.stdout.flush()

            with open(self._fpath) as fp:
                data = yaml.load(fp.read())

            for datapoint in data:
                item = self._data_type(**datapoint)
                db_session.add(item)

            db_session.flush()
            print("done.")

        else:
            print(
                "No {} found; skipping loading of {}s.".format(
                    self._fpath, self._data_type.__name__
                )
            )