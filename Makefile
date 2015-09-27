DOCKER=/usr/local/bin/docker
IMAGE=ksuderman/galaxy-lappsgrid

help:
	@echo "GOALS"
	@echo
	@echo "latest"
	@echo "    Builds Dockerfile"
	@echo "cmu"
	@echo "    Builds with services configured to call"
	@echo "    http://docker:8080."
	@echo "run"
	@echo "    Runs the $(IMAGE):cmu image"
	@echo "push"
	@echo "    Pushes $(IMAGE) to the Docker Hub."
	@echo "help"
	@echo "    Prints these usage instructions."
	@echo
	
cmu:
	$(DOCKER) build -f Dockerfile.cmu -t $(IMAGE):cmu .

latest:
	$(DOCKER) build -f Dockerfile -t $(IMAGE) .
	
#run:
#	$(DOCKER) run -d -p 8000:80 -p 9002:9002 --privileged=true $(IMAGE)
	
#run-cmu:
run:
	$(DOCKER) run -d --name galaxy --link vassar -p 8000:80 -p 9002:9002 --privileged=true $(IMAGE):cmu
	
push:
	$(DOCKER) push $(IMAGE)


