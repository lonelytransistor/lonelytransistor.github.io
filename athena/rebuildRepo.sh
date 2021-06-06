#!/bin/bash
rm Packages
mkdir -p tmp/
for fname in *.ipk ; do
    (
        cd tmp/
        tar zxf ../${fname}
        tar zxf control.tar.gz
        cat control >> ../Packages
    )
    md5=($(md5sum ${fname}))
    size=($(stat --format=%s ${fname}))

    echo -e "Filename: ${fname}" >> Packages
    echo -e "SHA256sum: ${md5}" >> Packages
    echo -e "Size: ${size}\n" >> Packages
done
gzip -k Packages
rm -rf tmp/
