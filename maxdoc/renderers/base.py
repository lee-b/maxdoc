import abc


class Renderer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def render(self, config, db_session, item):
        pass

    def __repr__(self):
        return self.__class__.__name__
