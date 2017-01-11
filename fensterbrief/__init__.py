# -*- coding: utf-8 -*-
#
#  Copyright 2016 Martin Schobert <martin@weltregierung.de>
#  

""" The main routine for the fensterbrief script """

import argparse
import configparser
import subprocess
import os
import sys
import shutil
from fensterbrief import fensterbrief
from fensterbrief.transmission.simple_fax_de.mail_to_simple_fax_de import mail_to_simple_fax_de
from fensterbrief.transmission.simple_fax_de.soap_to_simple_fax_de import soap_to_simple_fax_de
from fensterbrief.stamps.frank import frank

from pkg_resources import resource_stream, resource_listdir

def init_templates(config_file):

    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read(config_file)
    template_dir = config.get('DEFAULT', 'TEMPLATE_DIR')
      
    texmf_dir =  os.path.expanduser('~/texmf/tex/latex/fensterbrief/')

    # check if template directory exists
    if not os.path.exists(template_dir):
        answer = input("+ Shall directory %s be created? " % template_dir).lower()
        if 'y' in answer:
            os.makedirs(template_dir)
        else:
            return

    # create user's 'texmf' directory
    if not os.path.exists(texmf_dir):
        answer = input("+ Shall directory %s be created? " % texmf_dir).lower()
        if 'y' in answer:
            os.makedirs(texmf_dir)
        else:
            return
    
    # copy templates to tempalte directory
    for res_name in resource_listdir('templates', ''):
        if res_name.endswith(".tex") or res_name.endswith(".md") or res_name.endswith(".lco"):
            src_fd = resource_stream('templates', res_name)            

            if res_name.endswith(".tex") or res_name.endswith(".md"):
                dst_file = os.path.join(template_dir, res_name)
            else:
                dst_file = os.path.join(texmf_dir, res_name)
                
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

    # update
    subprocess.call(['texhash'])

                    
    
def init_config_file():
    
    # create a config file
    config = configparser.RawConfigParser()

    root_dir =     input("+ Root directory, where letters should be stored        : ")
    template_dir = input("+ Template directory, where template letters are stored : ")
    tex_editor =   input("+ Your preferred LaTeX editor                           : ")
    md_editor =    input("+ Your preferred Markdown editor                        : ")

    config['DEFAULT']['ROOT_DIR'] = root_dir
    config['DEFAULT']['TEMPLATE_DIR'] = template_dir
    config['DEFAULT']['TEX_EDITOR'] = tex_editor
    config['DEFAULT']['MD_EDITOR'] = md_editor

    return config

def init_google(config):
    print("+ In order to use the Google address lookup, we need a Google API key. You can request an API \n" +
          "  key from https://developers.google.com/maps/documentation/javascript/get-api-key .\n" +
          "  Sometimes you find API keys on github: \n" +
          "  https://github.com/search?o=desc&q=google+maps+api+key&ref=searchresults&s=indexed&type=Code")
    api_key = input("+ Your Google API key                                   : ")
    config['google']['api_key'] = api_key
    
def init_pandoc(config):
    config['pandoc']['program'] = 'pandoc'
    config['pandoc']['template'] = '${template_dir}/template-pandoc.tex'    

def init_modules(config):
    mail_from = input("+ Your e-mail address for simple-fax.de                 : ")
    password =  input("+ Your password for simple-fax.de                       : ")
            
    init_pandoc(config)
    init_google(config)
    mail_to_simple_fax_de.init_config(config)
    soap_to_simple_fax_de.init_config(config, mail_from, password)
    frank.init_config(config)
    

def main():

    # config
    config_file = os.path.expanduser('~/.fensterbrief.conf')

    # process command line arguments
    parser = argparse.ArgumentParser(description='A command line tool to prepare letters') 
    parser.add_argument('--list-templates', help='List all letter templates', action='store_true')
    parser.add_argument('--list-letters', help='List all letters', action='store_true')
    parser.add_argument('--search', help='Search for a string in filenames', metavar='STRING')
    parser.add_argument('--create-folder', help='Ask for meta data and create a new folder', action='store_true')
    parser.add_argument('--adopt', help='Create a new letter based on a previous one', metavar='FILE')
    parser.add_argument('--edit', help='Edit the current letter source file', action='store_true')
    parser.add_argument('--render', help='Render PDF file from current markdown or latex', action='store_true')
    parser.add_argument('--set-folder', help='Set the working folder', metavar='DIR')
    parser.add_argument('--mail-simple-fax', help='Send a fax via simple-fax.de using the e-mail interface', metavar='DEST')
    parser.add_argument('--soap-simple-fax', help='Send a fax via simple-fax.de using the SOAP interface', metavar='DEST')
    parser.add_argument('--buy-stamp', help='Buy a stamp. Place postage file in current folder or use together with --adopt.', nargs='?', metavar='PRODUCT_ID', const='1')

    parser.add_argument('--lookup-address', help='Search for an address via Gogle', metavar='STRING')    
    parser.add_argument('--keep-folder', help='Store the adopted letter in the same folder', action='store_true')
    parser.add_argument('--config', help='The configuration file to use', default=config_file, metavar='FILE')   
    parser.add_argument('--verbose', help='Show what is going on', action='store_true')
    parser.add_argument('--init', help='Initialize the environment', action='store_true')
    
    (options, args) = parser.parse_known_args()

    if options.init:

        if not os.path.exists(config_file):

            config = init_config_file()
            init_modules(config)

            with open(config_file, 'w') as cf_handle:
                print("+ Writing configuration file %s. You may want to edit this file later for further configuration." % config_file)
                config.write(cf_handle)
                os.chmod(config_file, 0o600)

            init_templates(config_file)            
                
        return

    
    # create default config file?
    if not os.path.isfile(config_file):
        print("+ Can't find config file. Please run: %s --init" % sys.argv[0])
        return
    
    # use a different config file?
    if options.config: 
        config_file = options.config
        
    # parse config
    if options.verbose:
        print("+ Reading config file %s" % options.config)


    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read([options.config])

    template_dir = config.get('DEFAULT', 'TEMPLATE_DIR')
    root_dir = config.get('DEFAULT', 'ROOT_DIR')

    if options.list_templates:
        fensterbrief.list_templates(template_dir, root_dir)

    elif options.list_letters:
        fensterbrief.list_letters(root_dir)

    elif options.search:
        fensterbrief.list_letters(root_dir, options.search)

    elif options.set_folder:
        print("+ Set working folder to %s" % options.set_folder)
        fensterbrief.write_working_ref(root_dir, options.set_folder)
        
    elif options.create_folder:
        recipient_name = fensterbrief.request_recipient()
        foldername = fensterbrief.request_folder(recipient_name)
        dst_folder_path = fensterbrief.create_folder(root_dir, foldername)

    elif options.adopt:
        address = None
        if options.lookup_address:
            address = fensterbrief.lookup_address(options.lookup_address, config)

        dst_file_name = fensterbrief.adopt(root_dir, options.adopt, options.keep_folder, address)

            
        if dst_file_name:
            if options.buy_stamp:
                f = frank.frank(config)
                f.buy_stamp(os.path.dirname(dst_file_name), options.buy_stamp)

            fensterbrief.edit_file(dst_file_name, config)
            
    elif options.buy_stamp: # after adopt
        working_ref = fensterbrief.load_working_ref(root_dir)
        f = frank.frank(config)
        outdir = os.path.join(root_dir, working_ref['dir'])
        f.buy_stamp(outdir, options.buy_stamp)

    elif options.edit:
        working_ref = fensterbrief.load_working_ref(root_dir)
        src_file = os.path.join(root_dir, working_ref['dir'], working_ref['src'])
        print("+ Edit file %s" % src_file)
        fensterbrief.edit_file(src_file, config)
        
    elif options.render:
        working_ref = fensterbrief.load_working_ref(root_dir)
        src_file = os.path.join(root_dir, working_ref['dir'], working_ref['src'])
        pdf_file = os.path.join(root_dir, working_ref['dir'], working_ref['pdf'])        

        print("+ Rendering file %s" % src_file)
        print("+ Output file %s" % pdf_file)
        
        if src_file.endswith('.tex'):
            subprocess.call(['latex', '-batch', src_file])           
        elif src_file.endswith('.md'):
            subprocess.call([config['pandoc']['program'], \
                             '--template', config['pandoc']['template'], \
                             '--output', pdf_file, src_file])
        else:
            print("+ Error: unknown file type for %s" % src_file)

        
    elif options.mail_simple_fax or options.soap_simple_fax:
      
        if options.mail_simple_fax:
            trans = mail_to_simple_fax_de(config)
        else:
            trans = soap_to_simple_fax_de(config)

        working_ref = fensterbrief.load_working_ref(root_dir)
        pdf_file = os.path.join(root_dir, working_ref['dir'], working_ref['pdf'])

        if options.mail_simple_fax:
            dst = options.mail_simple_fax
        else:
            dst = options.soap_simple_fax
            
        print("+ Going to send file: %s" % pdf_file)
        trans.send(pdf_file, dst, working_ref['pdf'])
        
    else:
        print("+ Unknown option")
        parser.print_help()

        
if __name__ == "__main__":
    main()

