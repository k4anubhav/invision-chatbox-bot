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

    @property
    def msg_id(self):
        return int(self._msg_id)

    @property
    def content(self):
        return replace_many(['\n', '\r', '\t'], self.raw_content, '')
