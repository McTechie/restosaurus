SHELL := /bin/zsh
.DEFAULT_GOAL := help

apispec: ## Update the OpenAPI spec
	@echo "\033[36mUpdating the OpenAPI spec...\033[0m"
	@python3 manage.py spectacular --file schema.yml
	@echo "\033[36mOpenAPI spec updated!\033[0m"

help: # Run `make help` to get help on the make commands
	@echo "\033[36mAvailable commands:\033[0m"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
