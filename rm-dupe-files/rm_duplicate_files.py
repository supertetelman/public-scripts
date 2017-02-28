#!/bin/env/python3

import hashlib
import os
import argparse


def get_checksum(filename):
    checksum = hashlib.md5()
    try:
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                checksum.update(chunk)
    except IOError:
        raise IOError
    return checksum.hexdigest()


def get_path(root, myfile):
    full_file = root + "\\" +  myfile # INFO: If run in python2 this may hit some unicode issues
    full_file = full_file.replace('\\','/')
    return full_file


def remove_dupes(same_folder_only = True, dry = False, directory = '.'):
    file_list = []
    print("About to start walking %s" %(directory))
    print("Are we only deleting files in the same directory? : %d"%(same_folder_only))
    print("Is this a dry run? : %d" %(dry))
    for root, subdirs, files in os.walk(directory):
        if same_folder_only:
            file_list = []
        for myfile in files:
            full_file = get_path(root, myfile)
            try:
                checksum = get_checksum(full_file)
                if checksum in file_list:
                    print("Duplicate found - deleting: %s"%(full_file))
                    if dry is False:
                        os.remove(full_file)
                else:
                    file_list.append(checksum)
            except IOError:
                print("Could not read filename %s"%(full_file))
            except WindowsError:
                print("Could not delete filename %s"%(full_file))
    print("Completed walk.")
    return file_list


def remove_dupes_same_folder_only():
    return remove_dupes(same_folder_only=True, dry=False)


parser = argparse.ArgumentParser(description='A simple utility to find ' +
    'duplicate files and remove them. Will search through all subdirectories ' + 
    'from the root folder and delete any duplicate files within the same ' +
    'directory. Duplicated are determine via md5 sum.')
parser.add_argument('-a', '--all', dest='same_folder_only', action='store_false',
    default=True, help='By default this utility will only remove ' +
    'files that are duplicated within the same folder. If this flag is ' + 
    'enabled duplicate files in any directory searched will be removed. ' +
    'The first file will be retained.')
parser.add_argument('-d', '--dry', dest='dry', action='store_true',
    default=False, help='Dry run, only print what would happen')
parser.add_argument('-D', '--directory', dest='directory', action='store',
    default='.',  help='The directory to run on. Default is ","')
args = parser.parse_args()


if __name__ == '__main__':
    remove_dupes(args.same_folder_only, args.dry, args.directory)

