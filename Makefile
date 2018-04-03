DOCKER=docker
IMAGE=lappsgrid/galaxy
#VOLUME=-v /Users/suderman/docker/galaxy:/export

TAG=dev

latest: PASSWORD = $(shell curl -sSL http://api.lappsgrid.org/password?length=16)	
latest: SECRET = $(shell curl -sSL http://api.lappsgrid.org/password?length=32\&chars=abcdef0123456789)
latest:
	$(DOCKER) build --build-arg PASSWORD=$(PASSWORD) --build-arg SECRET=$(SECRET) -t $(IMAGE) .

deiis:
	$(DOCKER) build -f Dockerfile.cmu -t $(IMAGE):cmu .

no-cache:
	$(DOCKER) build --no-cache -f Dockerfile -t $(IMAGE) .

test:
	docker build -f Dockerfile.test -t $(IMAGE) .
	
#latest:
#	$(DOCKER) build -f Dockerfile -t $(IMAGE) .

push:
	$(DOCKER) push $(IMAGE)

tag:
	if [ -z "$(TAG)" ] ; then @echo "TAG has not been defined." ;  fi
	if [ -n "$(TAG)" ] ; then $(DOCKER) tag $(IMAGE) $(IMAGE):$(TAG) ; $(DOCKER) push $(IMAGE):$(TAG) ; fi

run:
	docker run --name galaxy -d -p 80:80 -p 8000:8000 $(IMAGE)

login:
	docker exec -it galaxy /bin/bash

stop:
	docker rm -f galaxy

help:
	@echo "GOALS"
	@echo
	@echo "cmu"
	@echo "    Builds with services configured to call"
	@echo "    Dockerized services (default goal)."
	@echo "latest"
	@echo "    Builds Dockerfile"
	@echo "push"
	@echo "    Pushes $(IMAGE):cmu to the Docker Hub."
	@echo "tag"
	@echo "    Tags $(IMAGE):cmu on the Docker Hub."
	@echo "help"
	@echo "    Prints these usage instructions."
	@echo

