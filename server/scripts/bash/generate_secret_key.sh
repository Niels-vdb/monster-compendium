#!/bin/bash

# Function to generate a secret key.
generate_secret_key() {
    openssl rand -base64 64 | tr -dc 'a-zA-Z0-9'
}

# Puts generated key in  variable.
SECRET_KEY=$(generate_secret_key)
# Removes last index (=).
SECRET_KEY=${SECRET_KEY%?}

echo "Generated secret key: $SECRET_KEY"
echo "If this file does not execute properly please add secret key manualy"

# Create secret key and add it to the .env file
if grep -q "SECRET_KEY" .env ; then
    sed -i '' "s/^SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
else
    echo SECRET_KEY=$SECRET_KEY >> .env
fi

echo Secret key created in .env
