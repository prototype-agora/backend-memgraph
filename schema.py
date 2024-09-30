import strawberry
from strawberry import Schema
import datetime 
import typing
from typing import Optional, List
from models import AppUser, Quote, Comment, Source
from relations import Cites, On, In
from database import db


@strawberry.type
class AppUserType:
    id: int
    first_name: str


@strawberry.type
class PostType:
    appuser_id: int
    quote_id: int
    comment_id: int
    source_id: int

@strawberry.type
class CommentType:
    text: str

@strawberry.type
class QuoteType:
    id: Optional[int]
    text: Optional[str]
    comment: Optional[str | None]

@strawberry.type
class SourceResource:
    id: int
    link: Optional[str]
    title: Optional[str]
    quotes: Optional[List[QuoteType]]

@strawberry.type
class AppUserResource:
    id: int
    first_name: str
    sources: List[SourceResource]

@strawberry.type
class PostResource:
    source: SourceResource
    user: AppUserType


@strawberry.type
class Query:
    @strawberry.field
    async def getAppUser(self, first_name: str) -> AppUserType:
        results = db.execute_and_fetch(
            """
            MATCH (n: AppUser {first_name: "%s"}) RETURN n;
            """
            % (first_name)
        )
        resultL = list(results)
        appuser = resultL[0]["n"]

        return AppUserType(id=appuser._id, first_name=appuser.first_name)

    @strawberry.field
    async def getAppUsers(self) -> List[AppUserType]:
        results = db.execute_and_fetch(
            """
            MATCH (n: AppUser) RETURN n;
            """
        )
        resultList = list(results)
        user = []
        for resultItem in resultList:
            user.append(AppUserType(id=resultItem["n"]._id, first_name=resultItem["n"].first_name))

        return user


    @strawberry.field
    async def getPosts(self, ) -> List[PostResource]:
        results = db.execute_and_fetch(
                """
                MATCH (u: AppUser)-[r2]-(q: Quote)-[r1]-(s:Source),
                (q)-[r3]-(c: Comment) Return q,u,s,c, r1, r2, r3;
                """
            )
        resultList = list(results)
        posts = []
        quotes = []
        for post in resultList:
            user = AppUserType(id=post["u"]._id, first_name=post["u"].first_name)
            quotes.append(QuoteType(
                id=post["q"]._id,
                text=post["q"].text_,
                comment=post["c"].text_))
            source = SourceResource(
                id=post["s"]._id,
                link=post["s"].link,
                title=post["s"].title,
                quotes=quotes
            )
            posts.append(PostResource(
                source=source,
                user=user
                ))
        return posts

    @strawberry.field
    async def getQuotesFromUser(self, first_name: str) -> typing.List[QuoteType]:
        results = db.execute_and_fetch(
            """
            MATCH (u: AppUser {first_name: "%s"})-[any1]-(q: Quote)
            OPTIONAL MATCH (c: Comment)-[any2]->(q) RETURN q,c
            """
            % (first_name)
        )
        results_raw = list(results)
        quotes = []
        for res in results_raw:
            if (res["c"]==None):
                quotes.append(QuoteType(id=res["q"]._id, text=res["q"].text_, comment=""))
            else:
                quotes.append(QuoteType(id=res["q"]._id, text=res["q"].text_, comment=res["c"].text_))
        return quotes


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_AppUser(self, first_name: str) -> AppUserType:
        user = AppUser(first_name=first_name).save(db)
        return AppUserType(id=user._id, first_name=user.first_name)

    @strawberry.mutation
    async def create_Source(self, link: str, title: str) -> SourceResource:
        source = Source(link=link, title=title).save(db)
        return SourceResource(id=source._id, title="", link="", quotes=[])
    
    @strawberry.mutation
    async def create_UniqueAppUser(self, first_name: str) -> AppUserType:
        results = db.execute_and_fetch(
            """
            MATCH (n: AppUser {first_name: "%s"}) RETURN n;
            """
            % (first_name)
        )
        resultsL = list(results)
        if (len(resultsL)>0):
            user = resultsL[0]["n"]
        else:
            user = AppUser(first_name=first_name).save(db)
        return AppUserType(id=user._id, first_name=user.first_name)

    @strawberry.mutation
    async def create_Post(self, first_name: str, quote_text: str, comment_text: str, link: str, title: str) -> PostType:
        
        try:
            user = AppUser.get_by_key("first_name", first_name)
        except:
            user = AppUser(first_name=first_name).save(db)

        quote = Quote(text_=quote_text).save(db)
        Cites(
            _start_node_id=user._id,
            _end_node_id=quote._id,
            date="%s"%(datetime.datetime.now())
        ).save(db)

        comment = Comment(text_=comment_text).save(db)
        On(
            _start_node_id=comment._id,
            _end_node_id=quote._id,
            date="%s"%(datetime.datetime.now())
        ).save(db)
        try:
            source = Source.get_by_key("link",link)
        except:
            source = Source(link=link, title=title).save(db)
        In(
            _start_node_id=quote._id,
            _end_node_id=source._id,
        ).save(db)

        return PostType(appuser_id=user._id, quote_id=quote._id, comment_id=comment._id, source_id=source._id)

schema = Schema(query=Query, mutation=Mutation)
