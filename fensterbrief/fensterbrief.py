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
import re
import googlemaps

working_object_file = '.working_object.conf'

def list_templates(dir_name, rel_dir):
    print("+ Looking up templates in %s" % dir_name)
    list_files(dir_name, None, rel_dir)
                
def list_letters(dir_name, search=None):
    print("+ Looking up letters in %s" % dir_name)
    list_files(dir_name, search, dir_name)

def list_files(dir_name, search=None, rel_dir=None):
    for (dirpath, dirnames, filenames) in os.walk(dir_name):
        for file in sorted(filenames):
            if (file.endswith(".tex") or file.endswith(".md") )and (search == None or search.lower() in file.lower()):
                print("  + %s" % os.path.relpath(os.path.join(dirpath, file), rel_dir))
    

def write_working_ref(doc_root, working_dir, working_src_file=None, working_pdf_file=None):
    """ Write information about the working directory into a file """

    # if working dir is absolute, make a directory name relative to doc_root
    if os.sep in working_dir and os.path.exists(working_dir):
        working_dir = os.path.abspath(working_dir)
        working_dir = os.path.relpath(working_dir, doc_root)

    print("+ Change folder to %s" % working_dir)

    # derive PDF file name from LaTeX/MD filename
    if working_src_file != None and working_pdf_file == None:
        working_pdf_file = working_src_file.replace(".md", ".pdf").replace(".tex", ".pdf")
        print("+ PDF output file will be %s" % working_pdf_file)
    
    # create a config file
    config = configparser.RawConfigParser()

    config['DEFAULT']['dir'] = str(working_dir)
    config['DEFAULT']['src'] = str(working_src_file)
    config['DEFAULT']['pdf'] = str(working_pdf_file)

    file = os.path.join(doc_root, working_object_file)
    with open(file, 'w') as fh:
        config.write(fh)
        os.chmod(file, 0o600)


def load_working_ref(doc_root):
    config = configparser.ConfigParser()
    file = os.path.join(doc_root, working_object_file)

    config.read(file)
    return config['DEFAULT']

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
    return [filename, letter_subject]


def request_file_and_folder(recipient_name, filetype="tex"):
    recipient_name = request_recipient()
    foldername = request_folder(recipient_name)
    filename, subject = request_file(recipient_name, filetype)
    
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


def adopt(doc_root, src_file, keep_folder=False, address=None):

    recipient_name = request_recipient()

    if src_file.endswith(".tex"):
        new_filename, subject = request_file(recipient_name, 'tex')
    elif src_file.endswith(".md"):
        new_filename, subject = request_file(recipient_name, 'md')
    else:
        print("+ Unkown file suffix in %s. Can't process file." % src_file)
        return None

    # check source file name
    if not src_file.startswith("/"):
        src_file = os.path.join(doc_root, src_file)

    if keep_folder:        
        dst_folder_path = os.path.dirname(src_file)
    else:
        foldername = request_folder(recipient_name)
        dst_folder_path = create_folder(doc_root, foldername)
             
    # copy file
    dst_file_path = os.path.join(dst_folder_path, new_filename)
    print("+ Copy file %s to %s" % (src_file, dst_file_path))
    if dst_file_path.endswith(".tex"):
        shutil.copyfile(src_file,  dst_file_path)
    else:
        copy_and_adjust_md(src_file,  dst_file_path, { 'subject' : subject,
                                                       'to' : address})


    # store referene to working dir
    write_working_ref(doc_root, dst_folder_path, new_filename)
    
    return dst_file_path


def copy_and_adjust_md(src_file,  dst_file, replace_data={}):

    # Regexps taken from
    # https://github.com/waylan/Python-Markdown/blob/master/markdown/extensions/meta.py
    # that is also under a BSD licence
    
    META_RE = re.compile(r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)')
    META_MORE_RE = re.compile(r'^[ ]{4,}(?P<value>.*)')
    END_RE = re.compile(r'^(-{3}|\.{3})(\s.*)?')

    meta = {}
    just_copy_line = False
    key = None
    
    with open(src_file) as fin:
        with open(dst_file, 'w') as fout:
            
            for line in fin.readlines():

                if just_copy_line:
                    fout.write(line)
                else:
                    
                    m1 = META_RE.match(line)
                    if m1:

                        key = m1.group('key').lower().strip()
                        value = m1.group('value').strip()

                        if key in meta:
                            meta[key].append(value)
                        else:
                            meta[key] = [value]

                            
                    elif END_RE.match(line) and key != None:
                        
                        just_copy_line = True
                        #print(replace_data)
                        #print(meta)
                        
                        # replace data
                        for k in replace_data:
                            if k in meta:
                                meta[k] = replace_data[k]
                             
                        # dump yaml data
                        for k in meta:
                            if isinstance(meta[k], list):
                                if len(meta[k]) == 1:
                                    fout.write("%s: %s\n" % (k, meta[k][0]))
                                else:
                                    fout.write("%s:\n" % k)                             
                                    for l in meta[k]:
                                        fout.write("    %s\n" % l)
                            else:
                                fout.write("%s: %s\n" % (k, meta[k]))

                        fout.write(line)

                    elif META_MORE_RE.match(line):
                        m2 = META_MORE_RE.match(line)
                        if m2 and key:
                         
                            # Add another line to existing key
                            meta[key].append(m2.group('value').strip())
                         
                    else:
                        fout.write(line)

        
def edit_file(dst_file_name, config):
    key = None    
    if dst_file_name.endswith(".tex"):
        key = 'TEX_EDITOR'
    elif dst_file_name.endswith(".md"):
        key = 'MD_EDITOR'
    else:
        print("+ Unsupported file") # already catched by 'if dst_file_name'
        return 

    subprocess.call( config.get('DEFAULT', key).split() + [dst_file_name])
                

def gmaps_lookup_address(keyword, api_key):
    gm = googlemaps.Client(key=api_key)
    result = gm.places(keyword)

    hits = None
    
    if result and ('status' in result) and result['status'] == 'OK':
        hits = []
        for r in result['results']:
            print(r['name'])
            print(r['formatted_address'])
            hits.append([r['name']] + r['formatted_address'].split(', '))

    return hits



def print_address_lookup_hits(results, idx=None):
    counter = 0
    for i in results:

        if idx == None or (idx != None and counter == idx):
            print("+ #%d" % counter)
        
            for l in i:
                print("\t%s" % l)

        counter += 1
        
    
def lookup_address(keyword, config):
    
    hits = gmaps_lookup_address(keyword, config['google']['api_key'])
    if hits == None:
        print("+ An error occured.")
        return None
    else:
        print("+ Matches:")
        print_address_lookup_hits(hits)
        if len(hits) > 1:
            idx = int(input("Please select address: "))
            print_address_lookup_hits(hits, idx)
        else:
            idx = 0
            
        return hits[idx]
    
