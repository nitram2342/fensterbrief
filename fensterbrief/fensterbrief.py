#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2016 Martin Schobert <martin@weltregierung.de>
#  

import configparser
import os
from datetime import date
from slugify import slugify
import shutil


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
        os.chmod(config_file, 0o600)

