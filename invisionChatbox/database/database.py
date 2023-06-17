from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from invisionChatbox.database.objs import ChatboxRoomPosts


class Database:
    def __init__(self, db_url):
        self._engine = create_engine(db_url)
        self._session = sessionmaker(bind=self._engine)

    def get_session(self):
        return self._session()

    def get_engine(self):
        return self._engine

    def add_message(self, obj: 'ChatboxRoomPosts'):
        with self.get_session() as session:
            session.add(obj)
            session.commit()
