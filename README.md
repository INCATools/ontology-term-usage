# ontology_term_usage

Python wrapper to different clients to determine how a particular term is used.

One use case is for ontology developers who want to obsolete a term but need to know how it is used.

For example, if GO wanted to obsolete "apoptosis", GO editors could query for GO:0006915 and see
which ontologies use it.

For more context see:

 - [obo#1630](https://github.com/OBOFoundry/OBOFoundry.github.io/pull/1630)

Demo server (NOT STABLE):

* https://v61vbincq3.execute-api.us-east-1.amazonaws.com/staging/docs
* https://v61vbincq3.execute-api.us-east-1.amazonaws.com/staging/usage/GO:0006915


Services wrapped:

* ontobee
* ubergraph (subset of OBO)
* go (for annotations and go-cams)
* uniprot sparql endpoint (for annotations)

Planned:

* bioportal

For more details, see inline docs and tests

No CLI yet. We will implement using click

Demo:

```bash
poetry run pytest -s
```

## Caveats

It is actually quite hard to determine whether a term is used. Many ontologies do not put their "complete" versions forward as the main
URL that is loaded into services like OLS, Ontobee, Bioportal,
in particular, the inter-ontology axioms this tool queries may be missing.

Ubergraph gets around this partially by having its own configuration
that may load additional axioms - but ubergraph may not have all of obo

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

 - It may be better to wrap this into a generic obolibrary python package

