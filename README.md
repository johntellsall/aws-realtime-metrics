# Easy Kubernetes for Webapps (includes Cat Voting Booth)

Modern webapp development is... complex.  This tutorial demonstrates how to quickly get up to speed with Kubernetes, learning webapp development Best Practices along the way.

With cats.


![Cat Voting Booth](http://www.motherjones.com/wp-content/uploads/catsvoting2.jpg)

# run webapp in single Flask container


## build and run webapp

    docker build -t catvote . &&  docker run -p 5000:5000 catvote

## open webapp in browser

    open http://$(docker-machine ip):5000

