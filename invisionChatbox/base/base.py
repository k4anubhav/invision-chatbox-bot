import enum

from invisionChatbox.context import Context
from abc import ABC, abstractmethod


class Validator(ABC):
    @abstractmethod
    def validate(self, context: Context, *args, **kwargs) -> bool:
        return True


class HttpMethods(enum.Enum):
    get = 0
    post = 1
    delete = 2
    put = 3
    patch = 4
