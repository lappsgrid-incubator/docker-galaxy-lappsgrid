# Lappsgrid Galaxy Flavour 
#

FROM ubuntu:14.04

MAINTAINER Keith Suderman, suderman@cs.vassar.edu

ENV BARE=True
ENV TERM=xterm
ARG PASSWORD
ARG SECRET

RUN apt-get update && apt-get install -y python-software-properties software-properties-common
RUN add-apt-repository ppa:openjdk-r/ppa  
RUN apt-get update && apt-get install -y curl wget
RUN apt-get install -y git zip unzip emacs24-nox apt-transport-https ca-certificates

RUN sudo apt-get install -y openjdk-8-jdk #&& \
	#echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | sudo tee -a /etc/apt/sources.list.d/webupd8team-java.list && \
	#echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | sudo tee -a /etc/apt/sources.list.d/webupd8team-java.list && \
	#sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886 && \
	#sudo apt-get update && \
	#echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections && \
	#echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections && \
	#sudo apt-get -y install oracle-java8-installer && \
	#sudo update-java-alternatives -s java-8-oracle && \
	#sudo apt-get install -y oracle-java8-set-default

RUN mkdir /var/lib/lsd && \
	cd /var/lib/lsd && \
	wget http://downloads.lappsgrid.org/lsd-latest.tgz && \
	tar xzf lsd-latest.tgz && \
	rm lsd-latest.tgz && \
	chmod +x lsd && \
	cd /usr/local/bin && \
	ln -s /var/lib/lsd/lsd

RUN sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list' && \
	wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add - && \
	sudo apt-get update && \
	sudo apt-get install -y postgresql postgresql-contrib

RUN adduser galaxy --system --group && \
	cd /home/galaxy && \
	git clone http://github.com/lappsgrid-incubator/Galaxy.git galaxy && \
	git clone http://github.com/lappsgrid-incubator/GalaxyMods.git mods

# Save the database password in a safe location so the database can be accessed
# later if needed.
RUN echo "$PASSWORD" > /root/postgres.passwd && \
	echo "PASSWORD: $PASSWORD" && \
	echo "SECRET  : $SECRET"

# Now create the database using `sed` to inject the database password into the SQL script.
COPY ./db-setup.sql /root/init.sql
RUN service postgresql start && \
	cat /root/init.sql | sed "s/__DB_PASSWORD__/$PASSWORD/" | sudo -u postgres psql
	
# Ensure we are using the correct branch for Galaxy.
RUN cd /home/galaxy/galaxy && git checkout lapps

# Patch the galaxy.ini file with the port number, installation directory, database 
# password, and id_secret.
RUN cd /home/galaxy && wget http://downloads.lappsgrid.org/scripts/patch-galaxy-ini.sh && \
	chmod +x patch-galaxy-ini.sh && \
	./patch-galaxy-ini.sh /home/galaxy

# Make sure everything in /home/galaxy is owned by the galaxy user.
RUN chown -R galaxy:galaxy /home/galaxy

# Mark folders as imported from the host.
VOLUME ["/export/", "/data/", "/var/lib/docker"]

# Expose port 80 (webserver), 21 (FTP server), 8800 (Proxy)
EXPOSE :80
EXPOSE :21
EXPOSE :22
EXPOSE :8800
EXPOSE :9002

# Autostart script that is invoked during container start
ADD ./galaxy.sh /usr/bin/startup
CMD ["/usr/bin/startup"]    
    
