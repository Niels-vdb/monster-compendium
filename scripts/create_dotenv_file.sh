#!/bin/bash

# Checks if the .env file exists in the root of the program
# If it does not exist it will create a copy vrom .env.example
if [ ! -f ".env" ]; then
    echo ".env does not exists, copying .env.example"
    cp ".env.example" ".env"
    echo "Made a new copy of .env"
else
    echo ".env file does exists"
fi