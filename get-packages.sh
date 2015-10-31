# Since the .tgz packages are not kept in source control this script can be used
# to download the packages.

PACKAGE_LIST="lsd brat"

if [ ! -d packages ] ; then
	mkdir packages
fi

cd packages
rm lsd.tgz

for package in $PACKAGE_LIST ; do
	wget http://www.anc.org/downloads/docker/$package.tgz
done
