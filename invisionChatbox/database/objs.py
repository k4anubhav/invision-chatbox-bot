# orm mapped classes
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import *
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ChatboxRoomPost(Base):
    __tablename__ = 'chatbox_room_posts'

    __table_args__ = {'keep_existing': True}

    chat_id = Column(BIGINT(20, unsigned=True), primary_key=True, autoincrement=True)
    chat_content = Column(MEDIUMTEXT)
    chat_time = Column(INTEGER(11), default=0)
    chat_member_id = Column(BIGINT(20), default=0)
    chat_room = Column(INTEGER(11), default=0)
    chat_sys = Column(MEDIUMTEXT)
    chat_in_multiple_rooms = Column(VARCHAR(245))
    chat_guestName = Column(VARCHAR(255))
    chat_title = Column(VARCHAR(255))
    chat_title_furl = Column(VARCHAR(255))

    metadata = Base.metadata

    def __repr__(self):
        return f'<ChatboxRoomPosts(chat_id={self.chat_id}, chat_content={self.chat_content}, chat_time={self.chat_time}, chat_member_id={self.chat_member_id}, chat_room={self.chat_room}, chat_sys={self.chat_sys}, chat_in_multiple_rooms={self.chat_in_multiple_rooms}, chat_guestName={self.chat_guestName}, chat_title={self.chat_title}, chat_title_furl={self.chat_title_furl})>'
