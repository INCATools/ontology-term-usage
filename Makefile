RUN = poetry run

# serverless/lambda seems to require this be at root level
#APP_PATH = ontology_term_usage.app.main
APP_PATH = main

test:
	$(RUN) pytest -s

app:
	$(RUN) uvicorn $(APP_PATH):app --reload

# https://adem.sh/blog/tutorial-fastapi-aws-lambda-serverless
deploy:
	sls deploy --stage staging
