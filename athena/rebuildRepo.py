#!/usr/bin/env python
import tarfile, os, hashlib, re, gzip
from collections import OrderedDict as odict
from packaging import version as v

def hashFile(fName):
    md5 = hashlib.md5()
    with open(fName, 'rb') as f:
        while (data := f.read(65536)):
            md5.update(data)
    return md5.hexdigest()

def readControl(fName):
    print("Parsing", fName)
    with tarfile.open(fName, mode="r:gz") as tar:
        if not "./control.tar.gz" in tar.getnames():
            print("Malformed ipk!")
            return None
        with tarfile.open(fileobj=tar.extractfile("./control.tar.gz"), mode="r:gz") as ctar:
            if not "./control" in ctar.getnames():
                print("Malformed ipk!")
                return None
            ctrl = ctar.extractfile("./control").read().decode("utf-8")
            ctrl = ctrl + ("\nFilename: %s\nSHA256sum: %s\nSize: %d" % (fName, hashFile(fName), os.path.getsize(fName)))
            return odict([re.split("\s*:\s*", z, maxsplit=1) for z in re.split("\n+", ctrl)])

def readPackages(dirName):
    pkgs = {}
    for fName in os.listdir(dirName):
        if os.path.splitext(os.path.basename(fName))[1] == ".ipk":
            if pkg := readControl(fName):
                if pkg["Package"] in pkgs and v.parse(pkgs[pkg["Package"]]["Version"])<v.parse(pkg["Version"]):
                    print(" A newer version has been found.")
                    pkgs.update({pkg["Package"]: pkg})
                if not pkg["Package"] in pkgs:
                    pkgs.update({pkg["Package"]: pkg})
    return pkgs
                    
def writePackages(pkgs):
    packages = ""
    for pkgName in pkgs:
        for entry in pkgs[pkgName]:
            packages += "%s: %s\n" % (entry, pkgs[pkgName][entry])
        packages += "\n"
    return packages

repoDir = "."
pkgs = writePackages(readPackages(repoDir)).encode("utf-8")
with open(os.path.join(repoDir, "Packages"), "wb") as f:
    f.write(pkgs)
with open(os.path.join(repoDir, "Packages.gz"), "wb") as f:
    f.write(gzip.compress(pkgs))
