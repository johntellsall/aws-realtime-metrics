Mission Critical, Web Scale Cat Voting Booth

# build and run single Flask container

    docker build -t catvote . &&  docker run -p 5000:5000 catvote

Open webapp in browser

    open http://$(docker-machine ip):5000