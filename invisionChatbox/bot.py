import logging
import re
from time import sleep
from typing import List, Union

import requests

from .base.eventhandler import EventHandler
from .context import Context, ContextResponse

# TODO: Replace logger
logging.basicConfig(level=logging.INFO)


class Bot(EventHandler):
    """
    Bot Class
    Contains Funcs that usually use quite frequently and need all over the program
    """

    def __init__(
            self,
            username: str,
            bot_id: int,
            site_domain: str,
            csrf_key: str,
            cookie: str,
            room_id: int,
            plp_upload: str,
            file_room: str,
            room_name: str,
            interval: int = 1,
            https: bool = True,
            max_text_limit: int = 100,
            command_activator: str = '/',
            max_file_size: int = 104857600,
            self_reply: bool = False,
            online_status: bool = True,
            case_sensitive: bool = False
    ):
        super().__init__()
        self._show_ago_time: str = ''
        self.online_status = online_status
        self._lastId: int = 2
        self.site_domain: str = site_domain
        self.room_id = room_id
        self.self_reply = self_reply
        self.csrf_key = csrf_key
        self.interval = interval
        self.plp_upload = plp_upload
        self.username = username
        self.bot_id = bot_id
        self.file_room = file_room
        self.room_name = room_name
        self.command_activator = command_activator
        self.case_sensitive = case_sensitive
        self.max_file_size = max_file_size
        self.max_text_limit = max_text_limit
        self.cookie = cookie
        self.skip_q = True
        self._http = 'https' if https else 'http'

    @property
    def command_pattern(self):
        if self.case_sensitive:
            return re.compile(rf'^{self.command_activator}(?P<command>[a-zA-Z0-9]+)?', re.IGNORECASE)
        return re.compile(rf'^{self.command_activator}(?P<command>[a-zA-Z0-9]+)?')

    @property
    def headers(self):
        return {
            'authority': self.site_domain,
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': f'{self._http}://{self.site_domain}',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'{self._http}://{self.site_domain}/',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': self.cookie,
        }

    def command(self, event_name: Union[str, List[str]] = None, validators=None, is_command: bool = True):
        return self.event(event_name=event_name, validators=validators, is_command=is_command)

    @property
    def page_headers(self):
        return {
            'authority': f'{self.site_domain}',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': self.cookie,
        }

    @property
    def site_url(self):
        return f'{self._http}://{self.site_domain}'

    def get_latest_messages(self) -> ContextResponse:
        params = (
            ('app', 'chatbox'),
            ('module', 'chatbox'),
            ('controller', 'room'),
            ('id', self.room_id),
            ('joined', '1'),
            ('do', 'getMSG'),
        )

        data = {
            'csrfKey': self.csrf_key,
            'lastID': self._lastId,
            'first_load': '0',
            'loadMoreMode': '0',
            'isReconnect': '0'
        }

        response = requests.post(f'{self.site_url}/index.php', headers=self.headers, params=params,
                                 data=data, timeout=5)
        resp = ContextResponse(**response.json(), bot=self)
        if resp.last_id:
            self._lastId = resp.last_id
        return resp

    def send_message(self, message: str, tag: str = None, strip: bool = True) -> None:
        if strip:
            message = message[:self.max_text_limit]
        if isinstance(tag, str):
            if not tag.startswith('@'):
                tag = f'@{tag}'
            message = f'{tag} {message}'

        data = {
            'cbForm_submitted': '1',
            'csrfKey': self.csrf_key,
            'MAX_FILE_SIZE': self.max_file_size,
            'plupload': self.plp_upload,
            'chatMSG_' + f'{self.room_id}': message,
            'file_room_' + f'{self.room_id}': self.file_room
        }

        response = requests.post(f'{self.site_url}/chatbox/room/{self.room_id}-{self.room_name}/',
                                 headers=self.headers,
                                 data=data,
                                 timeout=5)
        if response.json() == 'OK':
            logging.info("Success while sending msg")
        else:
            logging.critical(str(response.json()) + "<< server error #sd2e")

    def send_direct_message(self, message: str, member_id: int, tag: str = None, strip: bool = True):
        if strip:
            message = message[:self.max_text_limit]
        if isinstance(tag, str):
            if not tag.startswith('@'):
                tag = f'@{tag}'
            message = f'{tag} {message}'

        conv_id, pl_upload, file_upload = self._open_conv(member_id=member_id)

        params = (
            ('app', 'chatbox'),
            ('module', 'conversation'),
            ('controller', 'main'),
            ('conID', conv_id),
            ('do', 'postEditor'),
        )

        data = {
            'cbForm_submitted': '1',
            'csrfKey': self.csrf_key,
            'MAX_FILE_SIZE': '104857600',
            'plupload': pl_upload,
            'chatCON_' + conv_id: message,
            'file_con_' + conv_id: file_upload
        }

        response = requests.post(f'{self.site_url}/index.php', headers=self.headers, params=params, data=data)
        assert response.status_code == 200
        print(response.text)

    def _open_conv(self, member_id: int):
        params = (
            ('app', 'chatbox'),
            ('module', 'conversation'),
            ('controller', 'main'),
            ('do', 'openConversation'),
        )

        data = {
            'csrfKey': self.csrf_key,
            'memberID': member_id,
            'conID': ''
        }
        response = requests.post(f'{self.site_url}/index.php', headers=self.headers, params=params, data=data)
        if response.status_code != 200:
            # TODO: custom exception
            raise Exception()
        data = response.json()
        if data.get('type') == 'error':
            # TODO: custom exception
            raise Exception()
        html = data['html']
        conv_id = data['conID']
        pl_upload = re.search(
            r'''name=['"]plupload['"][\d\D]*?value=['"](?P<plupload>[0-9a-z]+)['"]''',
            html).group('plupload')
        file_upload = re.search(
            r'''name=['"]file_con_\d+['"][\d\D]*?value=['"](?P<file_upload>[0-9a-z]+)['"]''',
            html).group('file_upload')
        return conv_id, pl_upload, file_upload

    def set_last_id(self):
        message_response = self.get_latest_messages()
        if message_response.last_id:
            self._lastId = message_response.last_id
        else:
            raise Exception('yo boi')

    def ping(self) -> bool:
        params = (
            ('app', 'chatbox'),
            ('module', 'chatbox'),
            ('controller', 'room'),
            ('id', self.room_id),
            ('joined', '1'),
            ('do', 'ping'),
        )

        data = {
            'csrfKey': self.csrf_key,
        }

        response = requests.post(f'{self.site_url}/index.php', headers=self.headers, params=params,
                                 data=data, timeout=5)

        logging.info(f"\r{response.text} <<ping reply")
        return True if response.text == 'OK' else False

    def handle_message(self, context: Context, data=None):
        if not data:
            data = {}
        if search_res := self.command_pattern.search(context.content):
            command = search_res.group('command')
            self.call_command(command, context, data=data)

        self.call_command('__non_command__', context, data=data)

    def run(self):
        if self.ping():
            print('Ping')
        p = 0
        while True:
            try:
                if self.skip_q:
                    self.set_last_id()
                    self.skip_q = False

                if self.online_status:
                    # fixme: do this acc to time
                    p += 1
                    if p > 80:
                        self.ping()
                        p = 0

                context_resp = self.get_latest_messages()
                for message in context_resp.content:
                    message: Context
                    if (not self.self_reply) and str(message.user_id) == str(self.bot_id):
                        continue
                    self.handle_message(message)
                sleep(self.interval)
            except Exception as e:
                print(e)
