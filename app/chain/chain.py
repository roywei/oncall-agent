#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------

import os

from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

#from langchain.llms import OpenAI

# Accessing an environment variable
api_key = os.getenv('OPENAI_API_KEY')

# Configuring LangChain with the environment variable
#llm = OpenAI(api_key=api_key)

# ----------------------------------------------------------------------------
# config & prompt template
# ----------------------------------------------------------------------------

model = ChatOpenAI(openai_api_key=api_key)

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

# ----------------------------------------------------------------------------
# chain (of ops)
# ----------------------------------------------------------------------------

chain = prompt | model

# ----------------------------------------------------------------------------
# functions
# ----------------------------------------------------------------------------

for s in chain.stream({"topic":"bears"}):
    print(s.content, end="", flush=True)

# ----------------------------------------------------------------------------
# Principle: Think of a tool as a prompt template which returns data or calls api
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# EOF
# ----------------------------------------------------------------------------