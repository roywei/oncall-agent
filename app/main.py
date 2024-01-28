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
    logging.info(f"Searching mongoDB for: {error_message}")

    solution = await mongoDB_vector_search(error_stack)
    logging.info(f"Found Solution: {solution}")
    logging.info("Found ")

import os
from dotenv import find_dotenv, dotenv_values
config = dotenv_values(find_dotenv())

api_key = os.getenv('OPENAI_API_KEY')
ATLAS_URI = os.getenv('ATLAS_URI')
DB_NAME = os.getenv('DB_NAME', default='devopsgpt')
from OpenAIClient import OpenAIClient

openAI_client = OpenAIClient (api_key=api_key)

ATLAS_URI = os.getenv('ATLAS_URI')
DB_NAME = os.getenv('DB_NAME', default='devopsgpt')
from AtlasClient import AtlasClient
import time

def do_vector_search (query:str) -> None:
    t1a = time.perf_counter()
    embedding = openAI_client.get_embedding(query)
    t1b = time.perf_counter()
    print (f"Getting embeddings from OpenAI took {(t1b-t1a)*1000:,.0f} ms")
    atlas_client = AtlasClient (ATLAS_URI, DB_NAME)
    t2a = time.perf_counter()
    reports = atlas_client.vector_search(collection_name="embeddings", index_name="report_index", attr_name='report_embedding', embedding_vector=embedding,limit=10 )
    t2b = time.perf_counter()

    print (f"Altas query returned {len (reports)} reports in {(t2b-t2a)*1000:,.0f} ms")
    print(reports)

    for idx, report in enumerate (reports):
        print(idx)
        print(report)
        print(report['_id'])
    return reports[0]['text']

async def mongoDB_vector_search_fake(query):
    # fake return load the file from local
    with open("/Users/Lai/Documents/workspace/oncall-agent/reports/Add_to_cart_error.txt", "r") as f:
        #return full file content
        return f.read()

async def mongoDB_vector_search(query):
    return do_vector_search(query)

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