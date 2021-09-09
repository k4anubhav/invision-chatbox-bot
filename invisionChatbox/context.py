from typing import List, Union

from .message import Message
from .utils.common import replace_many


class Context:
    def __init__(self, **kwargs):
        self.message: Message = kwargs.get('message')
        self.bot = kwargs.get('bot')

    @property
    def content(self):
        return self.message.content

    def reply(self, message: str, tag=None, dm=None, strip=True):
        if dm is None:
            dm = False
        if dm and tag is None:
            tag = False
        else:
            tag = True

        if not dm:
            self.bot.send_message(message, tag=self.message.username if tag else None, strip=strip)
        else:
            self.bot.send_direct_message(message, self.message.user_id, tag=self.message.username if tag else None,
                                         strip=strip)

    @property
    def clean_content(self):
        to_replace = ['\n', '\r', '\t']
        for command in self.bot.handlers.keys():
            to_replace.append(f'{self.bot.command_activator}{command}')
        return replace_many(to_replace, self.message.raw_content, '').strip()


class ContextResponse:
    def __init__(self, **kwargs):
        self.cache_level = cache_level if (cache_level := kwargs.get('cacheLevel')) and cache_level.isnumeric() else 0
        self.chatters = ...  # TODO: add chatters list
        bot = kwargs.get('bot')
        self.content: List[Context] = [Context(message=Message(**data), bot=bot) for data in kwargs.get('content')]
        self._last_id = kwargs.get('lastID')

    @property
    def last_id(self) -> Union[int, None]:
        if self._last_id:
            return int(self._last_id)
