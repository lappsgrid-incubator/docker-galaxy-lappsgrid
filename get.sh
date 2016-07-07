#!/bin/bash
set -e 

GALAXY=/Applications/Servers/Galaxy
TYPES=$GALAXY/lib/galaxy/datatypes
CONVERTERS=$TYPES/converters

if [ ! -d converters ] ; then
	mkdir converters
fi

while [ -n "$1" ] ; do
	case $1 in
		converters)
			echo "Copying converters"
			cp $CONVERTERS/gate_to_lif_converter.xml converters
			cp $CONVERTERS/lif_to_gate_converter.xml converters
			cp $CONVERTERS/gigaword2lif.xml converters
			cp $CONVERTERS/gigaword2lif.lsd converters
			cp $CONVERTERS/invoke.lsd converters
			;;
		types)
			echo "Copying text.py"
			cp $TYPES/text.py .
			echo "Copying datatypes_conf.xml"
			cp $GALAXY/config/datatypes_conf.xml .
			;;
		oaqa)
			echo "Copying OAQA tools."
			cp -R $GALAXY/tools/lapps_oaqa ./tools
			;;
		masc)
			echo "Copying MASC datasource."
			cp -R $GALAXY/tools/lapps_masc ./tools
			;;
		common)
			echo "Copying common services."
			cp -R $GALAXY/tools/lapps_common ./tools
			;;
		*)
			echo "Unknown option $1"
			exit 1
	esac
	shift
done


