# Lappsgrid Galaxy Flavour 
#

FROM bgruening/galaxy-stable:dev

MAINTAINER Keith Suderman, suderman@cs.vassar.edu

ENV GALAXY_CONFIG_BRAND="LAPPS Docker"

RUN apt-get update && apt-get install -y bash emacs24-nox

ADD ./packages/lsd.tgz /usr/bin/
RUN chmod a+x /usr/bin/lsd

#ADD ./welcome.html /galaxy-central/static/welcome.html
ADD ./welcome.html /galaxy-central/web/welcome.html
ADD ./tool_conf.xml /galaxy-central/config/tool_conf.xml
ADD ./tools /galaxy-central/tools
 
RUN echo "192.168.99.100 docker" >> /etc/hosts

WORKDIR /galaxy-central

RUN add-tool-shed --url 'https://testtoolshed.g2.bx.psu.edu/' --name 'Test Tool Shed'

# Mark folders as imported from the host.
VOLUME ["/export/", "/data/", "/var/lib/docker"]

# Expose port 80 (webserver), 21 (FTP server), 8800 (Proxy)
EXPOSE :80
EXPOSE :21
EXPOSE :22
EXPOSE :8800
EXPOSE :9002

# Autostart script that is invoked during container start
ADD ./startup.sh /usr/bin/startup
CMD ["/usr/bin/startup"]    
    
