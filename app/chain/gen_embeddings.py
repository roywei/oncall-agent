#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# general process is generate embeddings, store embeddings, query embeddings
# ----------------------------------------------------------------------------

import os

# from langchain.prompts import ChatPromptTemplate
# from langchain.chat_models import ChatOpenAI

from langchain_openai import OpenAIEmbeddings

#from langchain.llms import OpenAI

# Accessing an environment variable
api_key = os.getenv('OPENAI_API_KEY')

# ----------------------------------------------------------------------------
# Embeddings tutorial - goal is to generate the embeddings then store in DB
# ----------------------------------------------------------------------------

# https://python.langchain.com/docs/integrations/text_embedding/openai

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

text = "This is a test document."

query_result = embeddings.embed_query(text)

print(query_result[:5])


# ----------------------------------------------------------------------------
# EOF
# ----------------------------------------------------------------------------