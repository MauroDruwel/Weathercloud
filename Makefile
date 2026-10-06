.PHONY: all lint lint-openapi lint-fern docs generate generate-python generate-csharp generate-typescript generate-go generate-rust

all: lint docs generate

lint: lint-openapi lint-fern

lint-openapi:
	npx --yes @redocly/cli lint openapi.yaml --skip-rule operation-4xx-response

lint-fern:
	npx --yes fern-api check

docs:
	npx --yes @redocly/cli bundle openapi.yaml -o docs/openapi.json --ext json

generate:
	npx --yes fern-api generate --local --force

generate-python:
	npx --yes fern-api generate --group python-sdk --local --force

generate-csharp:
	npx --yes fern-api generate --group csharp-sdk --local --force

generate-typescript:
	npx --yes fern-api generate --group typescript-sdk --local --force --package

generate-go:
	npx --yes fern-api generate --group go-sdk --local --force

generate-rust:
	npx --yes fern-api generate --group rust-sdk --local --force
