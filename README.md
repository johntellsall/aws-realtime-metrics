# Easy Kubernetes for Webapps (includes Cat Voting Booth)

Modern webapp development is... complex.  This tutorial demonstrates how to quickly get up to speed with Docker and Kubernetes, learning webapp development Best Practices along the way.

With cats.


## First, start with a single Docker container

## setup

Ensure Docker VM is running

    docker-machine start

## build and run webapp


    docker build -t randocat . &&  docker run -p 5000:5000 randocat

## open webapp in browser

    open http://localhost:5000

## Then, add a database

# Troubleshooting

## Page doens't load in browser

This page isn’t working
localhost didn’t send any data.
ERR_EMPTY_RESPONSE

=> wrong IP
=> mark port EXPOSEd in Dockerfile
=> check code uses the same port that's EXPOSEd. Don't ask how I learned this one :)
=> Docker container isn't running
