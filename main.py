# TODO: figure out how to put this in the app/ folder and still use serverless
# This line: `handler: main.handler`
# How do we specify a path here, as per uvicorn?

import os
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from fastapi import FastAPI, Query

# for lambda; see https://adem.sh/blog/tutorial-fastapi-aws-lambda-serverless
from mangum import Mangum


from ontology_term_usage.term_usage import OntologyClient, ResultSet, TermUsage, TERM, ServiceMetadataCollection

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

@app.get("/metadata", response_model=ServiceMetadataCollection)
async def metadata() -> ServiceMetadataCollection:
    return client.get_services()

handler = Mangum(app)