#!/bin/bash

service postgresql start
until pg_isready &>/dev/null ; do
	echo -n "."
	sleep 2
done

cd /home/galaxy
./run.sh

