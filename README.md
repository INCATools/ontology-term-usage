# ontology_term_usage

Python wrapper to different clients to determine how a particular term is used.

One use case is for ontology developers who want to obsolete a term but need to know how it is used.

Services wrapped:

 * ontobee
 * ubergraph (subset of OBO)

Planned

 * go (for annotations and go-cams)
 * bioportal
 * uniprot sparql endpoint (for annotations)

For more details, see inline docs and tests

No CLI yet. We will implement using click

Demo:

```bash
poetry run pytest -s
```

## API

To run the API locally:

```bash
make app
```

 * Docs: http://127.0.0.1:8000/docs
 * Find usages: http://127.0.0.1:8000/usage/GO:0007588

Deployment on AWS via serverless:

Follow 

https://adem.sh/blog/tutorial-fastapi-aws-lambda-serverless

for serverless/lambda deployment

Type

```bash
make deploy
```

## Future plans

It may be better to wrap this into a generic obolibrary python package

## API

Make a simple API using fastapi
 
