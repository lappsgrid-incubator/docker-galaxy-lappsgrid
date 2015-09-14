# Lappsgrid Galaxy Flavour
#
# Version 0.1

FROM bgruening/galaxy-stable:15.05

MAINTAINER Keith Suderman, suderman@cs.vassar.edu

ENV GALAXY_CONFIG_BRAND Lapps

WORKDIR /galaxy-central
RUN mv /etc/ssl/private /etc/ssl/private.bak
RUN mkdir /etc/ssl/private
RUN cp  /etc/ssl/private.bak/ssl-cert-snakeoil.key /etc/ssl/private
RUN chown -R postgres:postgres /etc/ssl/private
RUN chmod -R 740 /etc/ssl/private

RUN ls -hal /etc/ssl
RUN ls -hal /etc/ssl/private

RUN add-tool-shed --url 'https://testtoolshed.g2.bx.psu.edu/' --name 'Test Tool Shed'
RUN install-repository \
    "--url https://testtoolshed.g2.bx.psu.edu/ -o ksuderman --name lapps_gate_2_0_0 --panel-section-name Gate"
#    "--url https://testtoolshed.g2.bx.psu.edu/ -o ksuderman --name masc_2_0_0 --panel-section-name Masc" \
#    "--url https://testtoolshed.g2.bx.psu.edu/ -o ksuderman --name lapps_stanford_2_0_0 --panel-section-name Stanford" 

# Mark folders as imported from the host.
#VOLUME ["/export/", "/data/", "/var/lib/docker"]

# Expose port 80 (webserver), 21 (FTP server), 8800 (Proxy)
#EXPOSE :80
#EXPOSE :21
#EXPOSE :8800
#EXPOSE :9002

# Autostart script that is invoked during container start
CMD ["/usr/bin/startup"]    
    