DOCKER=/usr/local/bin/docker
IMAGE=lappsgrid/galaxy
TARFILE=galaxy-lappsgrid-cmu.tar

latest:
	$(DOCKER) build -f Dockerfile -t $(IMAGE) .
	
cmu:
	$(DOCKER) build -f Dockerfile.cmu -t $(IMAGE):cmu .

no-cache:
	$(DOCKER) build --no-cache -f Dockerfile -t $(IMAGE) .

push:
	$(DOCKER) push $(IMAGE)

tag:
	if [ -n "$(TAG)" ] ; then $(DOCKER) tag $(IMAGE) $(IMAGE):$(TAG) ; fi

tag-cmu:
	if [ -n "$(TAG)" ] ; then $(DOCKER) tag $(IMAGE):cmu $(IMAGE):$(TAG) ; fi

run:
	$(DOCKER) run -d -p 8080:80 --name galaxy -v /mnt/sda1/var/lib/galaxy:/export $(IMAGE)

bash:
	$(DOCKER) run -it -p 8080:80 --name galaxy $(IMAGE) /bin/bash

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
	

