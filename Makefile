DOCKER=/usr/local/bin/docker
IMAGE=lappsgrid/galaxy
TARFILE=galaxy-lappsgrid-cmu.tar

help:
	@echo "GOALS"
	@echo
	@echo "latest"
	@echo "    Builds Dockerfile"
	@echo "cmu"
	@echo "    Builds with services configured to call"
	@echo "    http://vassar:8080."
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
	
upload:
	@echo "Saving container to a tar file."
	$(DOCKER) save -o $(TARFILE) $(IMAGE):cmu
	@echo "GZipping the tar file."
	gzip $(TARFILE)
	@echo "Uploading the gz file."
	scp -P 22022 $(TARFILE).gz suderman@anc.org:/home/www/anc/downloads/docker
	
push:
	$(DOCKER) push $(IMAGE)


