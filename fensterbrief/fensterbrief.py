#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2016 Martin Schobert <martin@weltregierung.de>
#  

import argparse
import configparser
import os
#from TexSoup import TexSoup
from datetime import date
from slugify import slugify
import shutil
import subprocess

# config
config_file = os.path.expanduser('~/.fensterbrief.conf')



def list_templates(dir_name):
    print("+ Looking up templates in %s" % dir_name)
    for (dirpath, dirnames, filenames) in os.walk(dir_name):
        for file in sorted(filenames):
            if file.endswith(".lco"):
                print("  + %s" % os.path.join(dirpath, file))
                
def list_letters(dir_name, show_path=False, search=None):
    print("+ Looking up letters in %s" % dir_name)
    for (dirpath, dirnames, filenames) in os.walk(dir_name):
        for file in sorted(filenames):
            if file.endswith(".tex") and (search == None or search.lower() in file.lower()):
                if show_path:
                    print("  + %s" % os.path.join(dirpath, file))
                else:
                    print("  + %s" % file)


#def texsoup_get(ts, key1, key2):
#    for i in ts.find_all(key1):
#        if i.args[0] == key2:
#            return i.args[1]
#
#    return None



#def parse_doc(file):
#
#    content = open(file)
#    soup = TexSoup(content)

#    for i in soup.children:
#        for i2 in i.children:
#            #for i3 in i2.children:
#            print("[%s]" % i2)
        


def adopt(doc_root, src_file):
    month_str = date.today().strftime("%Y-%m")
    date_str = date.today().isoformat()

    recipient_name = slugify(input("Recipient short name: "), separator="_")
    folder_subject = slugify(input("Folder subject: "), separator="_")
    letter_subject = slugify(input("Letter subject: "), separator="_")
    
    
    print("+ Folder subject: %s" % folder_subject)
    print("+ Letter subject: %s" % letter_subject)
    print("+ Recipient: %s" % recipient_name)

    foldername = "%s_%s-%s" % (month_str, recipient_name, folder_subject)
    filename = "%s_%s-%s.tex" % (date_str, recipient_name, letter_subject)

    
    # create directory
    dst_folder_path = os.path.join(doc_root, foldername)
    if not os.path.exists(dst_folder_path):
        print("+ Creating folder %s" % dst_folder_path)
        os.mkdir(dst_folder_path)
    else:
        print("+ Folder %s already exists. Skipping creation." % dst_folder_path)
    
    # copy file
    dst_file_path = os.path.join(dst_folder_path, filename)
    print("+ Copy file %s to %s" % (src_file, dst_file_path))
    shutil.copyfile(src_file,  dst_file_path)
    
    return dst_file_path


def init_config_file(config_file):
    config = ConfigParser.RawConfigParser()

    root_dir = input("Root directory, where letters should be stored: ")
    template_dir = input("Template directory, where template letters are stored: ")
    editor = input("Root directory, where letters should be stored: ")

    config.set('DEFAULT', 'ROOT_DIR', root_dir)
    config.set('DEFAULT', 'TEMPLATE_DIR', template_dir)
    config.set('DEFAULT', 'EDITOR', editor)
    
    with open(config_file, 'wb') as cf_handle:
        print("+ Wiriting configuration file %s" % config_file)
        config.write(cf_handle)
        os.chmod(config_file, 0600)
                                                                                         
    
def main():

    # process command line arguments
    parser = argparse.ArgumentParser(description='A command line tool to prepare letters') 
    parser.add_argument('--config', help='The configuration file to use', default=config_file)
    parser.add_argument('--list-templates', help='List all letter templates', action='store_true')
    parser.add_argument('--list-letters', help='List all letters', action='store_true')
    parser.add_argument('--show-path', help='Show full path for filenames', action='store_true')
    parser.add_argument('--search', help='Search for a string in filenames')
    parser.add_argument('--adopt', help='Create a new letter based on a previous one')
    #parser.add_argument('--parse', help='Parse a letter')
  
    (options, args) = parser.parse_known_args()

    # create or read config file
    if not os.path.isfile(config_file):
        init_config_file(config_file)

    # parse config
    print("+ Reading config file %s" % options.config)
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read([options.config])

    template_dir = config.get('DEFAULT', 'TEMPLATE_DIR')
    root_dir = config.get('DEFAULT', 'ROOT_DIR')

    if options.list_templates:
        list_templates(template_dir)

    elif options.list_letters:
        list_letters(root_dir, options.show_path)

    elif options.search:
        list_letters(root_dir, options.show_path, options.search)

    elif options.adopt:
        dst_file_name = adopt(root_dir, options.adopt)
        subprocess.call([config.get('DEFAULT', 'EDITOR'), dst_file_name])
        
    #elif options.parse:
    #    parse_doc(options.parse)

    else:
        print("+ Unknown option")

        
if __name__ == "__main__":
    main()
