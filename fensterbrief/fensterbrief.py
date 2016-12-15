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

from pkg_resources import resource_stream, resource_listdir


def list_templates(dir_name, show_path=False):
    print("+ Looking up templates in %s" % dir_name)
    list_files(dir_name, show_path)
                
def list_letters(dir_name, show_path=False, search=None):
    print("+ Looking up letters in %s" % dir_name)
    list_files(dir_name, show_path, search)

def list_files(dir_name, show_path=False, search=None):
    for (dirpath, dirnames, filenames) in os.walk(dir_name):
        for file in sorted(filenames):
            if file.endswith(".tex") and (search == None or search.lower() in file.lower()):
                if show_path:
                    print("  + %s" % os.path.join(dirpath, file))
                else:
                    print("  + %s" % file)
    

def adopt(doc_root, src_file, keep_folder=False):
    month_str = date.today().strftime("%Y-%m")
    date_str = date.today().isoformat()

    recipient_name = slugify(input("+ Recipient short name: "), separator="_")

    if not keep_folder:
        folder_subject = slugify(input("+ Folder subject: "), separator="_")
        foldername = "%s_%s-%s" % (month_str, recipient_name, folder_subject)

    letter_subject = slugify(input("+ Letter subject: "), separator="_")
    filename = "%s_%s-%s.tex" % (date_str, recipient_name, letter_subject)
    
    
    if not keep_folder:
        print("+ Folder subject: %s" % folder_subject)
    print("+ Letter subject: %s" % letter_subject)
    print("+ Recipient: %s" % recipient_name)

    
    # create directory
    if not keep_folder:
        dst_folder_path = os.path.join(doc_root, foldername)
    else:
        dst_folder_path = os.path.dirname(src_file)
        
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


def init(config_file):

    if not os.path.exists(config_file):
        init_config_file(config_file)
    init_templates(config_file)
    
        
def init_templates(config_file):


    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read(config_file)
    template_dir = config.get('DEFAULT', 'TEMPLATE_DIR')
      

    # check if template directory exists
    if not os.path.exists(template_dir):
        answer = input("+ Shall directory %s be created? " % template_dir).lower()
        if 'y' in answer:
            os.makedirs(template_dir)
        else:
            return
    
    # copy templates to tempalte directory
    for res_name in resource_listdir('templates', ''):
        if res_name.endswith(".tex") or res_name.endswith(".lco"):
            src_fd = resource_stream('templates', res_name)            
            
            dst_file = os.path.join(template_dir, res_name)
            print("+ Copy resource file to %s" % dst_file)

            write_file = False
            if os.path.exists(dst_file):
                answer = input("+ Shall %s be overwritten? " % dst_file).lower()
                if 'y' in answer:
                    write_file = True
            else:
                write_file = True

            if write_file:
                with open(dst_file, 'wb') as dst_fd:                
                    shutil.copyfileobj(src_fd, dst_fd)
                    
    
def init_config_file(config_file):
    
    # create a config file
    config = configparser.RawConfigParser()

    root_dir = input("+ Root directory, where letters should be stored: ")
    template_dir = input("+ Template directory, where template letters are stored: ")
    editor = input("+ Root directory, where letters should be stored: ")

    config.set('DEFAULT', 'ROOT_DIR', root_dir)
    config.set('DEFAULT', 'TEMPLATE_DIR', template_dir)
    config.set('DEFAULT', 'EDITOR', editor)
    
    with open(config_file, 'w') as cf_handle:
        print("+ Writing configuration file %s" % config_file)
        config.write(cf_handle)
        os.chmod(config_file, 0o600)


