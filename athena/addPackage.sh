#!/bin/bash
mkdir -p tmp/

for f in "$@" ; do
    (
        cd tmp/
        tar zxf ../$f
        tar zxf control.tar.gz
        cat control >> ../Packages
    )
    md5=($(md5sum $f))
    size=($(stat --format=%s $f))

    echo -e "SHA256sum: ${md5}" >> Packages
    echo -e "Size: ${size}\n" >> Packages
done
