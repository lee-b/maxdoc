import abc


class DataGatherer(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def gather_data(self, db_engine):
        pass
