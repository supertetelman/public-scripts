# Summary
This was a simple utility that I made for personal use.

The script is meant to be run and pointed at a directory thought to contain duplicate files. 

It will walk through all subdirectories and remove any file that appears twice within the same directory under different file names. Identical file names are determined via md5sum and the first found file is kept.

Additionally files can be deleted if duplicates are found anywher; but use of this feature is advised only with utmost care.

# Setup

This script uses native python3 libraries and requires no other installs.

The script may run on python2, but will have trouble parsing any non english file names.

