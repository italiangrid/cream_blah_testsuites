#!/bin/sh

if [  $# -le 3 ]; then 
        echo -e "\nUsage:\n$0 <package_name> <package_version> <spec_name_complete> <source_path> \n"
        exit 1  
fi  

rpm -qa | grep --silent rpm-build
ret_val=$?
if [ $ret_val -eq 0 ]; then
        echo "Package rpm-build is installed.Proceeding..."
else
        echo "This script depends on rpm-build package to work!Exiting..."
        exit 1
fi

mkdir -p ~/rpm
mkdir -p ~/rpm/BUILD
mkdir -p ~/rpm/RPMS
mkdir -p ~/rpm/SOURCES
mkdir -p ~/rpm/SPECS
mkdir -p ~/rpm/SRPMS
mkdir -p ~/rpm/tmp

#NOTE: Always put explicit path here! (i.e.: do not use ~/rpm)
# It appends to /home/bertocco/.rpmmacros every time it is used, so comment
# these rows after the first use
#echo "%packager Sara Bertocco sara.bertocco@pd.infn.it" > /home/bertocco/rpmmacros
#echo "%_topdir ${HOME}/rpm" >> /home/bertocco/.rpmmacros
#echo "%_tmppath ${HOME}/rpm/tmp" >> /home/bertocco/.rpmmacros

package_name $1
package_version $2
spec_name $3
source_path $4

#echo "Now create a directory with name: package_name-version_number"
#echo "under ~/rpm/SOURCES and copy all the package's files there."
mkdir -p ~/rpm/SOURCES/${package_name}-${package_version}
cp -r ${source_path}/* ~/rpm/SOURCES/${package_name}-${package_version}
cd ~/rpm/SOURCES
tar cvzf ${package_name}.tar.gz ${package_name}-${package_version}/

echo "Tarball created!"
#echo "Now create a spec file and place it under ~/rpm/SPECS."
cp ${spec_name} ~/rpm/SPECS
cd ~/rpm
rpmbuild -ba SPECS/${spec_name}

