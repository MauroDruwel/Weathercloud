.PHONY: all lint lint-openapi lint-fern docs generate generate-python generate-csharp generate-typescript generate-go

all: lint docs generate

lint: lint-openapi lint-fern

lint-openapi:
	npx --yes @redocly/cli lint openapi.yaml --skip-rule operation-4xx-response

lint-fern:
	npx --yes fern-api check

docs:
	npx --yes @redocly/cli bundle openapi.yaml -o docs/openapi.json --ext json

generate:
	npx --yes fern-api generate --local

generate-python:
	npx --yes fern-api generate --group python-sdk --local

generate-csharp:
	npx --yes fern-api generate --group csharp-sdk --local

generate-typescript:
	npx --yes fern-api generate --group typescript-sdk --local

generate-go:
	npx --yes fern-api generate --group go-sdk --local
