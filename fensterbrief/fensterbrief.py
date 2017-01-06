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
import subprocess

working_object_file = '.working_object.conf'

def list_templates(dir_name):
    print("+ Looking up templates in %s" % dir_name)
    list_files(dir_name)
                
def list_letters(dir_name, search=None):
    print("+ Looking up letters in %s" % dir_name)
    list_files(dir_name, search)

def list_files(dir_name, search=None):
    for (dirpath, dirnames, filenames) in os.walk(dir_name):
        for file in sorted(filenames):
            if (file.endswith(".tex") or file.endswith(".md") )and (search == None or search.lower() in file.lower()):
                print("  + %s" % os.path.relpath(os.path.join(dirpath, file), dir_name))
    

def write_working_ref(doc_root, working_dir, working_tex_file=None, working_pdf_file=None):
    """ Write information about the working directory into a file """

    # if working dir is absolute, make a directory name relative to doc_root
    if os.sep in working_dir and os.path.exists(working_dir):
        working_dir = os.path.abspath(working_dir)
        working_dir = os.path.relpath(working_dir, doc_root)

    print("+ Change folder to %s" % working_dir)

    # derive PDF file name from LaTeX filename
    if working_tex_file != None and working_pdf_file == None:
        working_pdf_file = working_tex_file.replace(".md", ".pdf")
        working_pdf_file = working_tex_file.replace(".tex", ".pdf")
    
    # create a config file
    config = configparser.RawConfigParser()

    config.set('DEFAULT', 'WORKING_DIR', working_dir)
    config.set('DEFAULT', 'WORKING_TEX_FILE', working_tex_file)
    config.set('DEFAULT', 'WORKING_PDF_FILE', working_pdf_file)

    file = os.path.join(doc_root, working_object_file)
    with open(file, 'w') as fh:
        config.write(fh)
        os.chmod(file, 0o600)


def load_working_ref(doc_root):
    config = configparser.ConfigParser()
    file = os.path.join(doc_root, working_object_file)

    config.read(file)
    return { 'dir' : config.get('DEFAULT', 'WORKING_DIR'),
             'tex' : config.get('DEFAULT', 'WORKING_TEX_FILE'),
             'pdf' : config.get('DEFAULT', 'WORKING_PDF_FILE') }

def request_recipient():
    recipient_name = slugify(input("+ Recipient short name: "), separator="_")
    return recipient_name


def request_folder(recipient_name):
    month_str = date.today().strftime("%Y-%m")
    folder_subject = slugify(input("+ Folder subject: "), separator="_")
    foldername = "%s_%s-%s" % (month_str, recipient_name, folder_subject)

    return foldername


def request_file(recipient_name, filetype="tex"):
    letter_subject = slugify(input("+ Letter subject: "), separator="_")
    filename = "%s_%s-%s.%s" % (date.today().isoformat(), \
                                recipient_name, letter_subject, filetype)
    return filename


def request_file_and_folder(recipient_name, filetype="tex"):
    recipient_name = request_recipient()
    foldername = request_folder(recipient_name)
    filename = request_file(recipient_name, filetype)
    
    return [foldername, filename]


def create_folder(doc_root, foldername):

    dst_folder_path = os.path.join(doc_root, foldername)
    
    if not os.path.exists(dst_folder_path):
        print("+ Creating folder %s" % dst_folder_path)
        os.mkdir(dst_folder_path)
    else:
        print("+ Folder %s already exists. Skipping creation." % dst_folder_path)

    # store referene to working dir
    write_working_ref(doc_root, dst_folder_path)

    return dst_folder_path


def adopt(doc_root, src_file, keep_folder=False):

    recipient_name = request_recipient()

    if src_file.endswith(".tex"):
        new_filename = request_file(recipient_name, 'tex')
    elif src_file.endswith(".md"):
        new_filename = request_file(recipient_name, 'md')
    else:
        print("+ Unkown file suffix in %s. Can't process file." % src_file)
        return None
    
    if keep_folder:        
        dst_folder_path = os.path.dirname(src_file)
    else:
        foldername = request_folder(recipient_name)
        dst_folder_path = create_folder(doc_root, foldername)
    
    # check source file name
    if not src_file.startswith("/"):
        src_file = os.path.join(doc_root, src_file)
         
    # copy file
    dst_file_path = os.path.join(dst_folder_path, new_filename)
    print("+ Copy file %s to %s" % (src_file, dst_file_path))
    shutil.copyfile(src_file,  dst_file_path)


    # store referene to working dir
    write_working_ref(doc_root, dst_folder_path, new_filename)
    
    return dst_file_path

        

