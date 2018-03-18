# INBOX

    minikube start

## verify Kubernetes cluster is running

    minikube status

## view Kubernetes Dashboard

    minikube dashboard

## verify minikube

    kubectl run hello-minikube --image=k8s.gcr.io/echoserver:1.4 --port=8080
    kubectl expose deployment hello-minikube --type=NodePort
    kubectl get pod
    # once pod is Running
    curl $(minikube service hello-minikube --url)

*Clean up*

    kubectl delete service hello-minikube
    kubectl delete deploy hello-minikube

## build Randocat Docker image

    docker build -t randocat:v2 .

## Ideas

- !! mount host folder https://github.com/kubernetes/minikube/blob/master/docs/host_folder_mount.md

- K8s w/ insecure/internal registries - https://github.com/kubernetes/minikube/blob/master/docs/insecure_registry.md


## TODO

* EFD (Elasticsearch, Fluentd, Kibana) https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/fluentd-elasticsearch

* Heapster monitoring https://kubernetes.io/docs/tasks/debug-application-cluster/resource-usage-monitoring/

* Node Problem Detector (e.g. NTP) https://github.com/kubernetes/node-problem-detector


# Easy Kubernetes for Webapps (includes Cat Voting Booth)

Modern webapp development is... complex.  This tutorial demonstrates how to quickly get up to speed with Kubernetes, learning webapp development Best Practices along the way.

With cats.


![Cat Voting Booth](http://www.motherjones.com/wp-content/uploads/catsvoting2.jpg)

# version 1D: run webapp in single Pyramid container (using Docker)

## setup

Ensure Docker VM is running

    docker-machine start

## build and run webapp


    docker build -t randocat . &&  docker run -p 5000:5000 randocat

## open webapp in browser

    open http://localhost:5000

# version 1K: run webapp in single Flask container (using Kubernetes)

## install

TODO explain pieces & WHY

- hypervisor
    + TBD

- Kubectl
    + https://kubernetes.io/docs/tasks/tools/install-kubectl/

- Minikube

    brew cask install minikube

    + https://github.com/kubernetes/minikube/releases


## setup

Point Docker to re-use Minikube's Docker environment:
    
    eval $(minikube docker-env)

    kubectl version
    XX will now output Client and Server versions, as it's talking to X


## develop webapp, the hard way

    XX docker run -it easykubernetes_app bash

X? Now that Kubernetes and Docker are talking together, let's rebuild our webapp, X


    XXX kubectl run randocat --image=randocat --port=5000
    kubectl expose deployment randocat --type=NodePort
    curl $(minikube service randocat --url)

Once our container is running, it's much easier to make changes. Edit code, rebuild the container image, then stuff it into the active deployment:

    perl -pi -e 's/World/Cat/' ./app.py
    egrep Hello app.py

    ID=$(date +%H%M)
    docker image build -t randocat:$ID .
    kubectl set image deployment randocat *=randocat:$ID
    curl $(minikube service randocat --url)

## develop webapp, the easy way

Instead of the above, we can use our extremely simple Makefile:

    {edit code here}
    make apply

## watch what the webapp is doing

Let's watch the pod run by streaming its logs to the terminal. Hit Control-C to take the terminal back.

XX which pod?


    kubectl logs -f randocat-5548ff6b6c-txwns
     * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    172.17.0.1 - - [23/Dec/2017 19:28:50] "GET / HTTP/1.1" 200 -

Open the X console, so we can watch as Kubernetes makes use of our new, mission-critical, web-scale cat voting booth webapp:

http://192.168.99.101:30000/#!/namespace/default?namespace=default
http://192.168.99.101:30000/#!/deployment/default/randocat?namespace=default


Open our webapp in a browser:

    open $(minikube service randocat --url)

References: 

- https://kubecloud.io/minikube-workflows-d7166e1da290

- https://www.mankier.com/1/kubectl-set-image


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



# INBOX

- `run-container` = higher level? https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#run-container

- reusing the Docker repos -- no more pushing/pulling!
https://github.com/kubernetes/minikube/blob/master/docs/reusing_the_docker_daemon.md

hidden verbosity flag

    kubectl  --v=8 version


containerized Robot Framework
https://github.com/cgowez/robot-docker

# Resources

https://www.datawire.io/docker-mac-kubernetes-ingress/

https://logz.io/blog/kubernetes-docker-mac/

excellent list of tips for Kubernetes 
https://kubernetes.io/docs/reference/kubectl/cheatsheet/





# Historical

## setup (non-Edge)

Point Docker to re-use Minikube's Docker environment:
    
    eval $(minikube docker-env)

    kubectl version
    XX will now output Client and Server versions, as it's talking to X

## XX re-use Docker daemon

    eval $(minikube docker-env)

Now we can see Kubernetes internal containers using normal Docker commands. Example:

    docker ps | egrep dash


# OUTBOX

        open http://$(docker-machine ip):5000
