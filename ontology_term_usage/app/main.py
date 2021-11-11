import os
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from fastapi import FastAPI, Query

# for lambda; see https://adem.sh/blog/tutorial-fastapi-aws-lambda-serverless
from mangum import Mangum


from ontology_term_usage.term_usage import OntologyClient, ResultSet, TermUsage, TERM

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

client = OntologyClient()

app = FastAPI(title='Ontology Usage API', openapi_prefix=openapi_prefix)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/usage/{term}", response_model=ResultSet)
async def usage(term: TERM) -> ResultSet:
    rs = client.term_usage(term)
    return rs

handler = Mangum(app)