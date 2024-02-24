from abc import ABC, abstractmethod


class FlushPolicy(ABC):
    @abstractmethod
    def is_flush_condition_set(self):
        pass

    @abstractmethod
    def flush(self):
        pass
