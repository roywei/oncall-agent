#!/usr/bin/env python3

from fastapi import FastAPI

# ----------------------------------------------------------------------------
# FastAPI as main entrypoint of the app for consumption
# ----------------------------------------------------------------------------

app = FastAPI()

# ----------------------------------------------------------------------------
# design goal: supply an intermediate proxy to RAG endpoint via fastAPI
# ----------------------------------------------------------------------------

# static response

static_response = {
    "text": "this response is static from the fastAPI nlg endpoint!",
    "buttons": [],
    "image": None,
    "elements": [],
    "attachments": []
}

# ----------------------------------------------------------------------------
# some initial endpoints
# ----------------------------------------------------------------------------


# root
@app.get("/")
async def root():
    return static_response

# listener for event emitter
@app.get("/incident/")
async def root():
    return static_response

# endpoint to trigger RAG pipeline
@app.get("/retrieve/")
async def root():
    return static_response


# ----------------------------------------------------------------------------
# enable post endpoint
# ----------------------------------------------------------------------------

# @app.post("/dynamic/")
# async def request_gpt(nlg: incomplete):
#     meta_response = static_response
#     return meta_response


# ----------------------------------------------------------------------------
# EOF
# ----------------------------------------------------------------------------