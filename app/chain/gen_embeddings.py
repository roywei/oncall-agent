#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# general process is generate embeddings, store embeddings, query embeddings
# ----------------------------------------------------------------------------

import os
import sys

from typing import Any, List

# from langchain.prompts import ChatPromptTemplate
# from langchain.chat_models import ChatOpenAI

from langchain_openai import OpenAIEmbeddings

#from langchain.llms import OpenAI

from AtlasClient import AtlasClient


# Accessing an environment variable
api_key = os.getenv('OPENAI_API_KEY')

ATLAS_URI = os.getenv('ATLAS_URI')
DB_NAME = os.getenv('DB_NAME', default='devopsgpt')

# ----------------------------------------------------------------------------
# Embeddings tutorial - goal is to generate the embeddings then store in DB
# ----------------------------------------------------------------------------

# https://python.langchain.com/docs/integrations/text_embedding/openai

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

def gen_embedding(text: str)->List[float]:
    return embeddings.embed_query(text)

def store_embedding(atlas_client: AtlasClient, v: List[float])->bool:
    # connect to MongoDB
    # insert an embedding vector
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 gen_embeddings.py <input_file>')
        sys.exit(1)
    # 1. connect to MongoDB
    atlas_client = AtlasClient (ATLAS_URI, DB_NAME)
    # 2. generate embeddings
    input_file = sys.argv[1]
    with open(input_file, mode='rt', encoding="utf-8") as f:
        text = f.read()
    v = gen_embedding(text)
    print(v[:5])
    # store embeddings
    #store_embedding(conn, v)
    atlas_client.close_connection()
