from basicclient import BasicClient
from invisionChatbox.database.database import Database
from invisionChatbox.database.objs import ChatboxRoomPost

class DatabaseWriteClient(BasicClient):
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
            database: Database,
            interval: int = 1,
            https: bool = True,
            max_text_limit: int = 100,
            command_activator: str = '/',
            max_file_size: int = 104857600,
            self_reply: bool = False,
            online_status: bool = True,
            case_sensitive: bool = False,
    ):
        super().__init__(
            username=username,
            bot_id=bot_id,
            site_domain=site_domain,
            csrf_key=csrf_key,
            cookie=cookie,
            room_id=room_id,
            plp_upload=plp_upload,
            file_room=file_room,
            room_name=room_name,
            interval=interval,
            https=https,
            max_text_limit=max_text_limit,
            command_activator=command_activator,
            max_file_size=max_file_size,
            self_reply=self_reply,
            online_status=online_status,
            case_sensitive=case_sensitive
        )
        self.database = database

    def send_raw_message(self, message: ChatboxRoomPost):
        """
        Use with caution, can send xss and other malicious code to the chatbox
        """
        self.database.add_message(message)

