#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import logging

# ----------------------------------------------------------------------------
# FastAPI as main entrypoint of the app for consumption
# ----------------------------------------------------------------------------

app = FastAPI()

# Set up CORS middleware options
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Allows all origins from localhost:3001
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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

class FrontendError(BaseModel):
    message: str
    stack: str
    info: dict  # Additional info if needed

# Set up logging
logging.basicConfig(level=logging.INFO)

# Endpoint to receive and log frontend errors
@app.post("/log-frontend-error/")
async def log_frontend_error(error: FrontendError):
    # Log the error to a file
    logging.error(f"Frontend Error: {error.message} | Stack: {error.stack} | Info: {error.info}")
    logging.info("Calling on-call agent...")
    await error_handler(error.message, error.stack)
    return {"detail": "Error logged successfully"}


async def error_handler(error_message, error_stack):
    # Log the error to a file
    logging.info(f"Trying to resolve error: {error_message}")
    solution = await mongoDB_vector_search_fake(error_stack)
    logging.info(f"Found Solution: {solution}")
    logging.info("Found ")


async def mongoDB_vector_search_fake(query):
    # fake return load the file from local
    with open("/Users/Lai/Documents/workspace/oncall-agent/reports/Add_to_cart_error.txt", "r") as f:
        #return full file content
        return f.read()

async def mongoDB_vector_search(query):
    pass

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