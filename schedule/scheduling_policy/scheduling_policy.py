from abc import ABC, abstractmethod


class SchedulingPolicy(ABC):
    @abstractmethod
    def apply_policy(self):
        pass