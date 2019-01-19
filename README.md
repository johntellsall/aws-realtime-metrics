# Easy Kubernetes for Webapps

Modern webapp development is... complex.  This tutorial demonstrates how to quickly get up to speed with Docker and Kubernetes, learning webapp development Best Practices along the way.

With cats.


## First, start with a single Docker container


## build and run webapp (Docker)

    docker build -t randocat . &&  docker run -p 6543:6543 randocat

## open webapp in browser

    open http://localhost:6543

## kill all containers

    docker kill $(docker ps -aq)


# Troubleshooting

## Page doesn't load in browser

This page isn’t working
localhost didn’t send any data.
ERR_EMPTY_RESPONSE

=> wrong IP
=> mark port EXPOSEd in Dockerfile
=> check code uses the same port that's EXPOSEd. Don't ask how I learned this one :)
=> Docker container isn't running
