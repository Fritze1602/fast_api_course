

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sys
from .database import engine
from . import models
from .routers import post, user, auth, vote


# Wenn eine Tabelle für ein Modell nicht besteht, wird sie angelegt! Nur für nicht alembic!!!
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# origion =["https://www.exovia.de"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standard types: https://docs.pydantic.dev/latest/usage/types/standard_types/

# From Pydantic -> This class is called a Schema.
# Defining the shape of our request
# Wir Stellen die Form Request und Response sicher!


# Route / Path Operations

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Warum kommst du nicht in mein fastapi land. Read the docs"}
