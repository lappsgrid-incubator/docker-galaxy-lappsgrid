# Lappsgrid Galaxy Flavour
#
# Version 0.1

FROM ksuderman/galaxy-stable:osx

MAINTAINER Keith Suderman, suderman@cs.vassar.edu

ENV GALAXY_CONFIG_BRAND LAPPS

RUN apt-get update && apt-get install -y bash emacs24-nox

ADD ./packages/lsd.tgz /usr/bin/
RUN chmod a+x /usr/bin/lsd

#ADD ./welcome.html /galaxy-central/static/welcome.html
ADD ./welcome.html /galaxy-central/web/welcome.html
ADD ./tool_conf.xml /galaxy-central/config/tool_conf.xml
COPY ./tools /galaxy-central/tools
 
WORKDIR /galaxy-central

RUN add-tool-shed --url 'https://testtoolshed.g2.bx.psu.edu/' --name 'Test Tool Shed'
#RUN install-repository \
#    "--url https://testtoolshed.g2.bx.psu.edu/ -o ksuderman --name lapps_gate_2_0_0 --panel-section-name Gate" \
#    "--url https://testtoolshed.g2.bx.psu.edu/ -o ksuderman --name masc_2_0_0 --panel-section-name Masc" \
#    "--url https://testtoolshed.g2.bx.psu.edu/ -o ksuderman --name lapps_stanford_2_0_0 --panel-section-name Stanford" 

# Mark folders as imported from the host.
VOLUME ["/export/", "/data/", "/var/lib/docker"]

# Expose port 80 (webserver), 21 (FTP server), 8800 (Proxy)
EXPOSE :80
EXPOSE :21
EXPOSE :22
EXPOSE :8800
EXPOSE :9002

# Autostart script that is invoked during container start
CMD ["/usr/bin/startup"]    
    
