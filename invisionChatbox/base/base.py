from invisionChatbox.context import Context
from abc import ABC, abstractmethod


class Validator(ABC):
    @abstractmethod
    def validate(self, context: Context, *args, **kwargs) -> bool:
        return True
