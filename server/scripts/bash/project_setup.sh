#!/bin/bash

# Check if pipenv is installed on machine
echo ""Checking for pipenv installation
./scripts/pipenv_installer.sh

# Runs the create .env file script
pipenv run sh scripts/create_dotenv_file.sh

# Runs the create secret key shell
pipenv run sh scripts/generate_secret_key.sh

# Inform the user to start a new shell in the pipenv environment
echo "To continue working on your project, take the following steps"
echo "Activate the pipenv shell with: pipenv shell"
echo "To install dev packages run: pipenv install --dev"

