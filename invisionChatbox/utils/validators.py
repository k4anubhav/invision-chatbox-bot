from re import Pattern

from invisionChatbox.base.basic import Validator


class RegexValidator(Validator):
    def __init__(self, pattern: Pattern):
        self.pattern = pattern

    def validate(self, *args, **kwargs):
        return all(self.pattern.search(str(arg)) for arg in args) and all(self.pattern.search(str(arg)) for arg in kwargs.values())
