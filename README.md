Mission Critical, Web Scale Cat Voting Booth

# Hack: run and build single Flask container

    docker build -t catvote . &&  docker run -p 5000:5000 catvote
