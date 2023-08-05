SHELL := /bin/zsh
.DEFAULT_GOAL := help

env: ## Create a virtual environment
	@echo "\033[36mCreating a virtual environment...\033[0m"
	@python3 -m venv env
	@echo "\033[36mVirtual environment created!\033[0m"

setup: ## Install the dependencies
	@echo "\033[36mInstalling the dependencies...\033[0m"
	@pip3 install -r requirements.txt
	@echo "\033[36mDependencies installed!\033[0m"

start: ## Run the development server
	@echo "\033[36mRunning the development server...\033[0m"
	@python3 manage.py runserver
	@echo "\033[36mDevelopment server running!\033[0m"

apispec: ## Update the OpenAPI spec
	@echo "\033[36mUpdating the OpenAPI spec...\033[0m"
	@python3 manage.py spectacular --file schema.yml
	@echo "\033[36mOpenAPI spec updated!\033[0m"

help: # Run `make help` to get help on the make commands
	@echo "\033[36mAvailable commands:\033[0m"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
