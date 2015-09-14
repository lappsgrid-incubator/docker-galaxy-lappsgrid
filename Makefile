help:
	@echo "Help is needed."
	
cmu:
	/usr/local/bin/docker build -f Dockerfile.cmu -t ksuderman/galaxy-lappsgrid:cmu .

latest:
	/usr/local/bin/docker build -f Dockerfile -t ksuderman/galaxy-lappsgrid .
