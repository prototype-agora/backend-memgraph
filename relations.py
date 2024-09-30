from typing import Optional
from gqlalchemy import Relationship


class ChatsWith(Relationship, type="CHATS_WITH"):
    last_chatted: str


class Speaks(Relationship, type="SPEAKS"):
    since: Optional[str]


class Cites(Relationship, type="CITES"):
    date: Optional[str]

class On(Relationship, type="ON"):
    date: Optional[str]

class In(Relationship, type="IN"):
    pass