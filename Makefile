# adapted from https://kubecloud.io/minikube-workflows-d7166e1da290

REPO=catvote
FLASK_PORT=5000
TIMESTAMP=tmp-$(shell date +%s )

all:

setup:
	kubectl run $(REPO) --image=$(REPO):1 --port=$(FLASK_PORT)
	kubectl expose deployment $(REPO) --type=NodePort

.PHONY: apply
apply:
	@eval $$(minikube docker-env) ; \
	docker image build -t $(REPO):$(TIMESTAMP) .
	kubectl set image deployment $(REPO) *=$(REPO):$(TIMESTAMP)

smoketest:
	curl $$(minikube service catvote --url)

clean:
	kubectl delete deploy,svc $(REPO)
