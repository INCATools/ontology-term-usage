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

# necessary for serverless/lambda
stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

client = OntologyClient()

description = """
Wraps multiple endpoints to query for all usages of a term, including

* Terms used in logical definitions in external ontologies
* Terms used in annotation of entities like genes and proteins
* Terms used in specialized annotation such as GO-CAMs
"""

app = FastAPI(title='Ontology Usage API',
              description=description,
              contact = {
                  "name": "Chris Mungall",
                  "url": "https://github.com/cmungall/ontology-term-usage",
                  "email": "cjmungall AT lbl DOT gov",
              },
              openapi_prefix=openapi_prefix)

tags_metadata = [
    {
        "name": "usages",
        "description": "Operations on term usages",
        "externalDocs": {
            "description": "External docs",
            "url": "https://github.com/cmungall/ontology-term-usage",
        },
    },
    {
        "name": "metadata",
        "description": "Operations to discover more information about system configuration.",
        "externalDocs": {
            "description": "External docs",
            "url": "https://github.com/cmungall/ontology-term-usage",
        },
    },
]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/usage/{term}", response_model=ResultSet, summary='Find usages of a term', tags=["usages"])
async def usage(term: TERM, limit: int = None) -> ResultSet:
    """
    Find all usages of an ontology term across multiple services.

    To obtain metadata on all services called, use the services endpoint

    Example terms: GO:0006915 (apoptotic process), RO:0000057 (has participant)

    \f
    :param term: URI or CURIE of a term.
    :param limit: maximum number of usages
    :return: usages broken down by service
    """
    rs = client.term_usage(term, limit=limit)
    return rs

@app.get("/metadata", response_model=ServiceMetadataCollection, tags=["metadata"])
async def metadata() -> ServiceMetadataCollection:
    return client.get_services()

handler = Mangum(app)