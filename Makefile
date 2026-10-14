.PHONY: all lint lint-openapi lint-fern docs generate generate-python generate-csharp generate-typescript generate-go generate-rust sync-assets

all: lint docs generate

lint: lint-openapi lint-fern

lint-openapi:
	npx --yes @redocly/cli lint openapi.yaml --skip-rule operation-4xx-response

lint-fern:
	npx --yes fern-api check

docs:
	npx --yes @redocly/cli bundle openapi.yaml -o docs/openapi.json --ext json

sync-assets:
	@echo "Overlaying SDK assets (workflows, configs, READMEs)..."
	@for sdk in python csharp typescript go rust; do \
		if [ -d "sdk-assets/$$sdk" ] && [ -d "sdks/$$sdk" ]; then \
			cp -rf sdk-assets/$$sdk/. sdks/$$sdk/; \
		fi \
	done

generate:
	npx --yes fern-api generate --local --force
	@$(MAKE) sync-assets

generate-python:
	npx --yes fern-api generate --group python-sdk --local --force --package
	@if [ -d "sdk-assets/python" ] && [ -d "sdks/python" ]; then cp -rf sdk-assets/python/. sdks/python/; fi

generate-csharp:
	npx --yes fern-api generate --group csharp-sdk --local --force
	@if [ -d "sdk-assets/csharp" ] && [ -d "sdks/csharp" ]; then cp -rf sdk-assets/csharp/. sdks/csharp/; fi

generate-typescript:
	npx --yes fern-api generate --group typescript-sdk --local --force --package
	@if [ -d "sdk-assets/typescript" ] && [ -d "sdks/typescript" ]; then cp -rf sdk-assets/typescript/. sdks/typescript/; fi

generate-go:
	npx --yes fern-api generate --group go-sdk --local --force
	@if [ -d "sdk-assets/go" ] && [ -d "sdks/go" ]; then cp -rf sdk-assets/go/. sdks/go/; fi

generate-rust:
	npx --yes fern-api generate --group rust-sdk --local --force
	@if [ -d "sdk-assets/rust" ] && [ -d "sdks/rust" ]; then cp -rf sdk-assets/rust/. sdks/rust/; fi

