# Lappsgrid Galaxy Flavour
#
# Version 0.2

#FROM ksuderman/galaxy-stable:osx
FROM bgruening/galaxy-stable
#FROM lappsgrid/ubuntu:postgres

MAINTAINER Keith Suderman, suderman@cs.vassar.edu

ENV GALAXY_CONFIG_BRAND LAPPS

RUN apt-get update && apt-get install -y bash emacs24-nox git

ADD ./packages/lsd.tgz /usr/bin
RUN chmod a+x /usr/bin/lsd
ADD ./packages/brat.tgz /galaxy-central/config/plugins/visualizations

#ADD ./index.html /galaxy-central/static/welcome.html
ADD ./tools /galaxy-central/tools
ADD ./tool_conf.xml /galaxy-central/config/tool_conf.xml
ADD ./tool_sheds_conf.xml /galaxy-central/config/tool_sheds_conf.xml
#ADD ./galaxy.ini /galaxy-central/config/galaxy.ini

#ADD ./startup.sh /usr/bin/startup

WORKDIR /galaxy-central

RUN add-tool-shed --url 'https://testtoolshed.g2.bx.psu.edu/' --name 'Test Tool Shed'
RUN install-repository \
    "--url https://testtoolshed.g2.bx.psu.edu/ -o ksuderman --name lapps_datatypes_1_0_0 --panel-section-name Converters" 
#    "--url https://testtoolshed.g2.bx.psu.edu/ -o ksuderman --name masc_2_0_0 --panel-section-name Masc" \
#    "--url https://testtoolshed.g2.bx.psu.edu/ -o ksuderman --name lapps_stanford_2_0_0 --panel-section-name Stanford" 

# Mark folders as imported from the host.
VOLUME ["/export/", "/data/", "/var/lib/docker"]

# Expose port 80 (webserver), 21 (FTP server), 8800 (Proxy)
EXPOSE :80
EXPOSE :21
EXPOSE :22
EXPOSE :8000
EXPOSE :8800
EXPOSE :9002

# Autostart script that is invoked during container start
CMD ["/usr/bin/startup"]    
    
