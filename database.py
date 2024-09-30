from gqlalchemy import Memgraph

db = Memgraph("127.0.0.1", 7687, "testuser123", "t123")

async def init_db():
    db.drop_database()
    db.drop_indexes()
