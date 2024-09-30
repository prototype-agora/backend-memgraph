from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL

from schema import schema

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Welcome to the Student API"}


app.add_route("/graphql", GraphQL(schema))

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)