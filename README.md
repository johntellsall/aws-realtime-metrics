# Easy Kubernetes for Webapps (includes Cat Voting Booth)

Modern webapp development is... complex.  This tutorial demonstrates how to quickly get up to speed with Kubernetes, learning webapp development Best Practices along the way.

With cats.


![Cat Voting Booth](http://www.motherjones.com/wp-content/uploads/catsvoting2.jpg)

# version 1D: run webapp in single Flask container (using Docker)

## build and run webapp

    docker build -t catvote . &&  docker run -p 5000:5000 catvote

## open webapp in browser

    open http://$(docker-machine ip):5000

# version 1K: run webapp in single Flask container (using Kubernetes)

    kubectl version
    XX will now output Client and Server versions, as it's talking to X

Run a local container image registry. Our webapp runs on port 5000 by default, which conflicts with the registry, so let's move the registry:

    docker run -d -p 9999:5000 --restart always --name registry registry:2

X? Now that Kubernetes and Docker are talking together, let's rebuild our webapp, and push to the local container image registry.

    docker build -t catvote .
    docker tag catvote localhost:9999/catvote
    docker push localhost:9999/catvote

Now our webapp is built into an image, and the image is stored in a registry so Kubernetes can use it.

Open the X console, so we can watch as Kubernetes makes use of our new, mission-critical, web-scale cat voting booth webapp:

http://192.168.99.101:30000/#!/namespace/default?namespace=default
http://192.168.99.101:30000/#!/deployment/default/catvote?namespace=default

    kubectl run catvote --image=localhost:9999/catvote --port=5000
    kubectl expose deployment catvote --type=NodePort
    curl $(minikube service catvote --url)

Open our webapp in a browser:

    open $(minikube service catvote --url)


# SETUP

## XX Install Kubernetes

Parts: kubectl, minikube, VM (xhyve) 
XX WHY

https://kubernetes.io/docs/tasks/tools/install-kubectl/#before-you-begin
https://kubernetes.io/docs/getting-started-guides/minikube/#installation

### Install Kubernetes for macOS with Brew

    brew install kubectl

Verify kubectl is installed:

    kubectl version

The version will be output, so kubectl is installed correctly. It will also complain about connection refused, as we haven't told it where our Kubernetes cluster is. That's fine.

Start the cluster:

    minikube start

Verify Kubernetes is up:

    $ minikube status
    minikube: Running
    cluster: Running
    kubectl: Correctly Configured: pointing to minikube-vm at {ip}

Just for fun, create and run a service, verifying it's up with a command-line browser (curl) and a normal web browser:

    kubectl run hello-minikube --image=gcr.io/google_containers/echoserver:1.4 --port=8080
    kubectl expose deployment hello-minikube --type=NodePort
    curl $(minikube service hello-minikube --url)

It works, yay!  Check it with a normal web browser:

    open $(minikube service hello-minikube --url)

Now that we have a running app, let's view our cluster:

    minikube dashboard

Yay! That was fun. Okay, clean up our simple webapp:

    kubectl delete deployment hello-minikube

## XX re-use Docker daemon

    eval $(minikube docker-env)

Now we can see Kubernetes internal containers using normal Docker commands. Example:

    docker ps | egrep dash


# INBOX

containerized Robot Framework
https://github.com/cgowez/robot-docker
