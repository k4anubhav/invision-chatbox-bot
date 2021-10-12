from typing import List

import requests

from invisionChatbox.base.base import HttpMethods
from invisionChatbox.basicclient import BasicClient
from invisionChatbox.exceptions import APIException


class ApiClient(BasicClient):
    """
    While using any method make sure your apikey have access to perform certain task
    """

    def __init__(
            self,
            api_key: str,
            api_base_url: str,
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
        """
        :param api_key: api key
        :type api_key: str
        :param api_base_url: base url for api example :  https://example.com/api/
        :type api_base_url: str
        """
        super(ApiClient, self).__init__(username,
                                        bot_id,
                                        site_domain,
                                        csrf_key,
                                        cookie,
                                        room_id,
                                        plp_upload,
                                        file_room,
                                        room_name,
                                        interval,
                                        https,
                                        max_text_limit,
                                        command_activator,
                                        max_file_size,
                                        self_reply,
                                        online_status,
                                        case_sensitive)
        self.api_key = api_key
        self.api_base_url = api_base_url.strip().strip('/')

    @property
    def api_params(self):
        return {'key': self.api_key}

    def get_api_response(self, endpoint: str, method: HttpMethods, params: dict = None, data: dict = None):
        if params:
            params.update(self.api_params)

        if method == HttpMethods.patch:
            res = requests.patch(f'{self.api_base_url}{endpoint}', params=params, data=data)
        elif method == HttpMethods.post:
            res = requests.post(f'{self.api_base_url}{endpoint}', params=params, data=data)
        elif method == HttpMethods.delete:
            res = requests.delete(f'{self.api_base_url}{endpoint}', params=params, data=data)
        elif method == HttpMethods.put:
            res = requests.put(f'{self.api_base_url}{endpoint}', params=params, data=data)
        else:
            res = requests.get(f'{self.api_base_url}{endpoint}', params=params, data=data)

        if res.status_code != 200:
            raise APIException()

        return res.json()

    def get_user_data(self, user_id: int):
        return self.get_api_response(f'/core/members/{user_id}', method=HttpMethods.get)

    def get_user_groups(self, user_id: int):
        data = self.get_user_data(user_id)
        groups = [grp for grp in data['secondaryGroups']]
        groups.append(data['primaryGroup'])
        return groups

    def send_invision_message(self, title, body, to_user_id: List[int], from_user_id: int):
        return self.get_api_response('/core/messages', method=HttpMethods.post, data={
            'key': self.api_key,
            'from': from_user_id,
            'to': f'{to_user_id}',
            'title': title,
            'body': body
        })
