# Since the .tgz packages are not kept in source control this script can be used
# to download the packages.

PACKAGE_LIST="lsd-latest brat svm_rank_linux64"

if [ ! -d packages ] ; then
	mkdir packages
fi

cd packages
rm *.tgz

for package in $PACKAGE_LIST ; do
	wget http://www.anc.org/downloads/docker/$package.tgz
done
