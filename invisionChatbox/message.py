from typing import List, Union

from .bot import Bot
from .utils.common import safe_get, replace_many


class Message:
    def __init__(self, **kwargs):
        self._msg_id = int(kwargs.get('id'))
        self.can_del = True if kwargs.get('canDelete') else False
        self.can_edit = True if kwargs.get('canEdit') else False
        self.can_report = True if kwargs.get('canReport') else False
        self.user_id = kwargs.get('chatterID')
        self.username = kwargs.get('chatterName')
        self.system: bool = True if kwargs.get('sys') else False
        self.profile_pic = kwargs.get('chatterPhoto')
        self.name_format = kwargs.get('chatterNameFormat')
        self.raw_content: str = safe_get(kwargs, 'content', str, '')
        self.donation: bool = True if kwargs.get('sys') == '1' else False
        self.time_str: str = kwargs.get('time')
        self.bot: Bot = kwargs.get('command')

    @property
    def msg_id(self):
        return int(self._msg_id)

    @property
    def content(self):
        return replace_many(['\n', '\r', '\t'], self.raw_content, '')

    @property
    def clean_content(self):
        to_replace = ['\n', '\r', '\t']
        for command in self.bot.handlers.keys():
            to_replace.append(f'{self.bot.command_activator}{command}')
        return replace_many(to_replace, '')

    def reply(self, message: str, tag=True):
        return self.bot.send_message(message, self.username if tag else None)


class MessageResponse:
    def __init__(self, **kwargs):
        self.cache_level = cache_level if (cache_level := kwargs.get('cacheLevel')) and cache_level.isnumeric() else 0
        self.chatters = ...
        bot = kwargs.get('bot')
        self.content: List[Message] = [Message(**data, bot=bot) for data in kwargs.get('content')]
        self._last_id = kwargs.get('lastID')

    @property
    def last_id(self) -> Union[int, None]:
        if self._last_id:
            return int(self._last_id)
