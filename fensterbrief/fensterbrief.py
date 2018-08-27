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

def is_markdown(filename):
    if filename.endswith(".md"):
        return True
    else:
        return False

def is_latex(filename):
    if filename.endswith(".tex"):
        return True
    else:
        return False
    
    
    
def program_exists(program):
    """ Returns True if a program path exists or a program was found in the $PATH environment."""
    if shutil.which(program) is not None or os.path.exists(program):
        return True
    else:
        return False

def run_program(program, param_list=None):
    """ Run program, print status messages and return either
        None - if program does not exist,
        False - if program failed,
        True - if program was successful.

        If program name contains spaces, this indicates that there are additional params."""
    
    splitted = program.split()
    program = splitted[0]

    if len(splitted) > 1:
        param_list = splitted[1:] + param_list
        
    if param_list:
        call_args = [program] + param_list
    else:
        call_args = [program]

    if not program_exists(program):
        print("+ Error: Program %s does not exist. Please install the program or adjust your configuration file." % program)
        return None

    print("+ Going to execute %s" % call_args)
    ret = subprocess.call(call_args)

    # Return values are evaluated according to best practises. Further
    # testing will reveal, if 
    if ret != 0:
        if ret < 0:
            print("+ Program %s killed by signal %d." % (program, -ret))
        else:
            print("+ Program %s failed with return code %d." % (program, ret))
        return False
    else:
        print("+ Program %s returned sucessfully." % program)
        return True

    
def prompt(headline, default, new_config, old_config, config_section, config_key):

    print("+ %s" % headline)
    print("  ---------------------------------------------------------------")
    if default:
        print("  Default value: %s" % default)

    if old_config and config_section in old_config and config_key in old_config[config_section]:
        print("  Current value: %s" % old_config.get(config_section, config_key))
        if default:
            print("  Enter: keep current configuration, 'd': use default configuration")
        else:
            print("  Enter: keep current configuration")
    elif default:
        print("  Enter: use default configuration")
    else:
        print("  Enter: leave empty")
        
    result = input("  > ")

    if result == "":
        if old_config and config_section in old_config and config_key in old_config[config_section]:
            result = old_config.get(config_section, config_key)
        elif default:
            result = default
        else:
            result = None
    elif result == "d" and default:
        result = default
    else:
        result = None

    print("+ Use value: %s\n" % result)

    if config_section not in new_config:
        new_config[config_section] = {}
        
    new_config.set(config_section, config_key, result)

    
def list_templates(dir_name, rel_dir):
    print("+ Looking up templates in %s" % dir_name)
    list_files(dir_name, None, rel_dir)
                
def list_letters(dir_name, search=None):
    print("+ Looking up letters in %s" % dir_name)
    list_files(dir_name, search, dir_name)

def list_files(dir_name, search=None, rel_dir=None):
    for (dirpath, dirnames, filenames) in os.walk(dir_name):
        for file in sorted(filenames):
            if (is_latex(file) or is_markdown(file) )and (search is None or search.lower() in file.lower()):
                print("  + %s" % os.path.relpath(os.path.join(dirpath, file), rel_dir))
    

def write_working_ref(doc_root, working_dir=None, working_src_file=None, working_pdf_file=None):
    """ Write information about the working directory into a file """

    if working_dir is None and working_src_file is not None:
        working_dir = os.path.dirname(os.path.abspath(working_src_file))
        print("+ Derived folder path %s from source file %s" % (working_dir, working_src_file))

    # if working dir is absolute, make a directory name relative to doc_root
    if working_dir is not None and os.sep in working_dir and os.path.exists(working_dir):
        working_dir = os.path.abspath(working_dir)
        working_dir = os.path.relpath(working_dir, doc_root)

    print("+ Change folder to %s" % working_dir)

    # derive PDF file name from LaTeX/MD filename
    if working_src_file is not None and working_pdf_file is None:
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

def get_default(defaults, key):
    if defaults is not None and key in defaults and defaults[key] is not None and defaults[key] != "":
        return str(defaults[key])
    else:
        return None
    
def request_recipient(defaults=None):
    recipient_shortname = get_default(defaults, "recipient-shortname")
    if recipient_shortname:
        prompt = "+ Recipient short name (default: %s): " % recipient_shortname
    else:
        prompt = "+ Recipient short name: " 

    raw_input = input(prompt)

    if raw_input == "":
        raw_input = recipient_shortname
        
    return slugify(raw_input, separator="_")


def request_folder(recipient_name, defaults=None):
    month_str = date.today().strftime("%Y-%m")
    folder_subject = slugify(input("+ Folder subject: "), separator="_")
    foldername = "%s_%s-%s" % (month_str, recipient_name, folder_subject)

    return foldername


def request_file(recipient_name, filetype="tex", defaults=None):

    default_subject = get_default(defaults, "subject")
    if default_subject:
        prompt = "+ Letter subject (default: %s): " % default_subject
    else:
        prompt = "+ Letter subject: "
        
    letter_subject_raw = input(prompt)
    if letter_subject_raw == "":
        letter_subject_raw = default_subject
        
    
    letter_subject = slugify(letter_subject_raw, separator="_")
    filename = "%s_%s-%s.%s" % (date.today().isoformat(), \
                                recipient_name, letter_subject, filetype)
    return [filename, letter_subject_raw]


#def request_file_and_folder(recipient_name, filetype="tex", defaults=None):
#    recipient_name = request_recipient(defaults)
#    foldername = request_folder(recipient_name, defaults)
#    filename, subject = request_file(recipient_name, filetype, defaults)
 
#    return [foldername, filename]


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


def expand_file_name(path, doc_root):
    ''' Check parameter and expand it to a file name. '''

    if not path.startswith("/"):
        return os.path.join(doc_root, path)
    else:
        return path

    
def adopt(doc_root, src_file, keep_folder=False, address=None):

    recipient_name = None

    defaults = None
    
    src_file = expand_file_name(src_file, doc_root)

    # try to load some information from markdown file.
    if is_markdown(src_file):
        if defaults is None:
            defaults = {}
        yaml = read_yaml_from_md(src_file)
        for yaml_key in ['recipient-shortname', 'subject']:
            if yaml_key in yaml:                    
                defaults[yaml_key] = yaml[yaml_key]
            else: # should that be the default?
                defaults[yaml_key] = ""
            
    recipient_name = request_recipient(defaults)
        

    if is_latex(src_file):
        new_filename, subject = request_file(recipient_name, 'tex', defaults)
    elif is_markdown(src_file):
        new_filename, subject = request_file(recipient_name, 'md', defaults)
    else:
        print("+ Unkown file suffix in %s. Can't process file." % src_file)
        return None

    print("+ New filename is %s" % new_filename)
    
    if keep_folder:        
        dst_folder_path = os.path.dirname(src_file)
    else:
        foldername = request_folder(recipient_name)
        dst_folder_path = create_folder(doc_root, foldername)
             
    # copy file
    dst_file_path = os.path.join(dst_folder_path, new_filename)
    print("+ Copy file %s to %s" % (src_file, dst_file_path))
    if is_latex(dst_file_path):
        shutil.copyfile(src_file,  dst_file_path)
    else:
        replace_data = { 'subject' : subject,
                         'recipient-shortname' : recipient_name}
        if address:
            replace_data['to'] = address
            
        copy_and_adjust_md(src_file,  dst_file_path, replace_data)


    # store referene to working dir
    write_working_ref(doc_root, dst_folder_path, new_filename)
    
    return dst_file_path


# Regexps taken from
# https://github.com/waylan/Python-Markdown/blob/master/markdown/extensions/meta.py
# that is also under a BSD licence
    
META_RE = re.compile(r'^[ ]{0,3}(?P<key>[\#A-Za-z0-9_-]+):\s*(?P<value>.*)\s*')
META_MORE_RE = re.compile(r'^[ ]{4,}(?P<value>.*)')
END_RE = re.compile(r'^(-{3}|\.{3})(\s.*)?')

def read_yaml_from_md(file):

    key = None
    meta = {}
    
    with open(file) as fin:
        for line in fin.readlines():
            m1 = META_RE.match(line)
            m2 = META_MORE_RE.match(line)
                    
            if m1:

                key = m1.group('key').lower().strip()
                value = m1.group('value').strip()

                if value != '|':
                    if key in meta:
                        meta[key].append(value)
                    else:
                        meta[key] = value

            elif m2:

                if key:
                    value = m2.group('value').strip()
                            
                    if key in meta:
                        meta[key].append(value)
                    else:
                        meta[key] = [value]                                

                            
                elif END_RE.match(line) and key is not None:
                    return meta

    return meta
        
def copy_and_adjust_md(src_file,  dst_file, replace_data={}):


    meta = {}
    just_copy_line = False
    key = None

    key_order = []

    print(replace_data)
    
    with open(src_file) as fin:
        
        with open(dst_file, 'w') as fout:
            
            for line in fin.readlines():

                if just_copy_line:
                    fout.write(line)
                else:
                    
                    m1 = META_RE.match(line)
                    m2 = META_MORE_RE.match(line)
                    
                    if m1:

                        key = m1.group('key').lower().strip()
                        value = m1.group('value').strip()

                        if value != '|':
                            if key in meta:
                                meta[key].append(value)
                            else:
                                key_order.append(key)
                                meta[key] = [value]

                    elif m2:

                        if key:
                            value = m2.group('value').strip()
                            
                            if key in meta:
                                meta[key].append(value)
                            else:
                                key_order.append(key)
                                meta[key] = [value]                                

                            
                    elif END_RE.match(line) and key is not None:
                        
                        just_copy_line = True
                        #print(replace_data)
                        #print(meta)
                        
                        # replace data
                        for k in replace_data:
                            if k not in meta:
                                key_order.append(k)
                            meta[k] = replace_data[k] # replace

                                
                        # dump yaml data
                        for k in key_order:
                            if isinstance(meta[k], list):
                                if len(meta[k]) == 1:
                                    fout.write("%s: %s\n" % (k, meta[k][0]))
                                else:
                                    fout.write("%s: |\n" % k)                             
                                    for l in meta[k]:
                                        fout.write("    %s  \n" % l)
                            else:
                                fout.write("%s: %s\n" % (k, meta[k]))

                        fout.write(line)

                         
                    else:
                        fout.write(line)

def cat_file(fname):
    with open(fname) as fin:
        print(fin.read())
    
    
def edit_file(dst_file_name, config):
    key = None    
    if is_latex(dst_file_name):
        key = 'TEX_EDITOR'
    elif is_markdown(dst_file_name):
        key = 'MD_EDITOR'
    else:
        print("+ Unsupported file") # already catched by 'if dst_file_name'
        return 

    run_program(config.get('DEFAULT', key), [dst_file_name])
                

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

        if idx is None or (idx is not None and counter == idx):
            print("+ #%d" % counter)
        
            for l in i:
                print("\t%s" % l)

        counter += 1
        
    
def lookup_address(keyword, config):
    
    hits = gmaps_lookup_address(keyword, config['google']['api_key'])
    if hits is None:
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
    
