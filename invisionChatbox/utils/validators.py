import enum
import re
from re import Pattern

from invisionChatbox.base.base import Validator
from invisionChatbox.context import Context


class RegexSearchOn(enum.Enum):
    content = 1
    clean_content = 2
    raw_content = 3


class SystemCheckBy(enum.Enum):
    """
    Prefer `sys_content_type` cause its most stable and accurate
    """
    sys_content_type = 1
    user_id = 2
    both_sys_and_user_id = 3


class RegexValidator(Validator):
    def __init__(self, pattern: Pattern, search_on: RegexSearchOn = RegexSearchOn.content):
        self.pattern = pattern
        self.search_on = search_on

    def validate(self, context: Context, *args, **kwargs) -> bool:
        if self.search_on == RegexSearchOn.clean_content:
            return True if self.pattern.search(context.clean_content) else False
        elif self.search_on == RegexSearchOn.raw_content:
            return True if self.pattern.search(context.message.raw_content) else False
        else:
            return True if self.pattern.search(context.content) else False


class SystemValidator(Validator):

    def __init__(self, check_by: SystemCheckBy):
        self.check_by = check_by

    def validate(self, context: Context, *args, **kwargs) -> bool:
        if self.check_by == SystemCheckBy.sys_content_type:
            return context.message.system
        elif self.check_by == SystemCheckBy.user_id:
            return True if context.user_id == -1 else False
        else:
            return True if (context.message.system and (True if context.user_id == -1 else False)) else False


class TaggedValidator(Validator):
    def __init__(self, tag: str):
        self.tag = tag

    def validate(self, context: Context, *args, **kwargs) -> bool:
        if re.search(f"\b@{self.tag}\b", context.message.raw_content):
            return True
        return False


class SelfTaggedValidator(Validator):

    def validate(self, context: Context, *args, **kwargs) -> bool:
        if re.search(f"\b@{context.bot.username}\b", context.message.raw_content):
            return True
        return False
