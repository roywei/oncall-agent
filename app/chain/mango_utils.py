from dotenv import find_dotenv, dotenv_values
config = dotenv_values(find_dotenv())
import os
ATLAS_URI = config.get('ATLAS_URI')
if not ATLAS_URI:
    raise Exception ("'ATLAS_URI' is not set.  Please set it above to continue...")

api_key = os.getenv('OPENAI_API_KEY')

ATLAS_URI = os.getenv('ATLAS_URI')
DB_NAME = os.getenv('DB_NAME', default='devopsgpt')
from AtlasClient import AtlasClient

from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

from OpenAIClient import OpenAIClient

openAI_client = OpenAIClient (api_key=api_key)

import time

# Handy function
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


if __name__ == '__main__':
    do_vector_search ("Add to Cart Functionality Failure")