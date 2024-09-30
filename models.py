from gqlalchemy import Node, Field, match, create
from database import db
from typing import Optional


class AppUser(Node):
    first_name: str = Field(exists=True, db=db)

    def get_by_key(key: str, value: str):
        results = db.execute_and_fetch(
            """
            MATCH (n: AppUser {%s: '%s'}) RETURN n;
            """ %(key, value)
        )
        return list(results)[0]["n"]


class Streamer(AppUser):
    first_name: Optional[str] = Field(exists=True, db=db)
    followers: Optional[str]


class Language(Node, index=True, db=db):
    name: str = Field(unique=True, db=db)


class Quote(Node):
    text_: Optional[str] = Field(exists=True, db=db)

class Comment(Node):
    text_: Optional[str] = Field(exists=True, db=db)

class Source(Node):
    title: str = Field(exists=True, db=db)
    link: str = Field(exists=True, db=db)
    
    def get_by_key(key: str, value: str):
        results = db.execute_and_fetch(
            """
            MATCH (n: Source {%s: '%s'}) RETURN n;
            """ %(key, value)
        )
        return list(results)[0]["n"]
