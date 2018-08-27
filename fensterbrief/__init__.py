# -*- coding: utf-8 -*-
#
#  Copyright 2016 Martin Schobert <martin@weltregierung.de>
#  

""" The main routine for the fensterbrief script """

import argparse
import configparser
import os
import sys
import shutil
from fensterbrief import fensterbrief
from fensterbrief.transmission.simple_fax_de import mail_to_simple_fax_de
from fensterbrief.transmission.simple_fax_de import soap_to_simple_fax_de
from fensterbrief.stamps.frank import frank

from pkg_resources import resource_stream, resource_listdir, get_distribution


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
        if res_name.endswith(".tex") or res_name.endswith(".md") or res_name.endswith(".lco") or res_name.endswith(".sty"):
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
    fensterbrief.run_program('texhash')

   
def init_config_file(old_config):
    
    # create a config file
    config = configparser.RawConfigParser()

    fensterbrief.prompt("Root directory, where letters should be stored",
                        os.path.expanduser("~/Documents/letters/"),
                        config, old_config, "DEFAULT", "ROOT_DIR")

    fensterbrief.prompt("Template directory, where template letters are stored",
                        "${ROOT_DIR}/_templates/",
                        config, old_config, "DEFAULT", "TEMPLATE_DIR")
                   
    fensterbrief.prompt("Your preferred LaTeX editor",
                        "texmaker", config, old_config, "DEFAULT", "TEX_EDITOR")

    fensterbrief.prompt("Your preferred Markdown editor",
                        "emacs -nw", config, old_config, "DEFAULT", "MD_EDITOR")

    fensterbrief.prompt("Your preferred PDF viewer",
                        "evince", config, old_config, "DEFAULT", "PDF_VIEWER")


    if not fensterbrief.program_exists(config.get("DEFAULT", "TEX_EDITOR")):
        print("+ Error: tex editor does not exist. Please install it before using fensterbrief.")

    if not fensterbrief.program_exists(config.get("DEFAULT", "MD_EDITOR")):
        print("+ Error: Markdown editor does not exist. Please install it before using fensterbrief.")

    if not fensterbrief.program_exists(config.get("DEFAULT", "PDF_VIEWER")):
        print("+ Error: The PDF viewer does not exist. Please install it before using fensterbrief.")


    return config

def init_google(config, old_config):

    fensterbrief.prompt("In order to use the Google address lookup, we need a Google API key. \n" +
                        "  You can request an API key from: \n" +
                        "  https://developers.google.com/maps/documentation/javascript/get-api-key\n" +
                        "  Sometimes you find API keys on github: \n" +
                        "  https://github.com/search?o=desc&q=google+maps+api+key&ref=searchresults&s=indexed&type=Code",
                        None, config, old_config, 'google', 'api_key')
    
def init_pandoc(config, old_config):

    fensterbrief.prompt("The pandoc program",
                        "pandoc", config, old_config, "pandoc", "program")

    fensterbrief.prompt("The standard LaTeX template when rendering markdown",
                        "${template_dir}/template-pandoc.tex",
                        config, old_config, "pandoc", "template")

    if not fensterbrief.program_exists(config.get("pandoc", "program")):
        print("+ Error: The program 'pandoc' does not exist. Please install it before using fensterbrief.")

def init_latex(config, old_config):
    
    fensterbrief.prompt("Your preferred LaTeX program",
                        "latex", config, old_config, "latex", "program")

    if not fensterbrief.program_exists(config.get("latex", "program")):
        print("+ Error: The LaTeX program does not exist. Please install it before using fensterbrief.")

def init_modules(config, old_config):

    init_pandoc(config, old_config)
    init_latex(config, old_config)
    init_google(config, old_config)

    mail_to_simple_fax_de.init_config(config, old_config)
    soap_to_simple_fax_de.init_config(config, old_config)
    frank.init_config(config, old_config)
    

def main():

    # config
    config_file = os.path.expanduser('~/.fensterbrief.conf')

    # process command line arguments
    parser = argparse.ArgumentParser(description='Manage letters via command line')
    parser.add_argument('--list-templates', help='List all letter templates', action='store_true')
    parser.add_argument('--list-letters', help='List all letters', action='store_true')
    parser.add_argument('--search', help='Search for a string in filenames', metavar='STRING')
    parser.add_argument('--create-folder', help='Ask for meta data and create a new folder', action='store_true')
    parser.add_argument('--adopt', help='Create a new letter based on a previous one', metavar='FILE')
    parser.add_argument('--edit', help='Edit the current letter or another source file', metavar='FILE', nargs='?', const='')
    parser.add_argument('--render', help='Render PDF file from current markdown or latex', metavar='FILE', nargs='?', const='')
    parser.add_argument('--show-pdf', help='Open PDF file in PDF viewer', metavar='FILE', nargs='?', const='')
    parser.add_argument('--set-folder', help='Set the working folder', metavar='DIR')
    parser.add_argument('--cat', help='Dump content of a letter', metavar='FILE')    
    parser.add_argument('--mail-simple-fax', help='Send a fax via simple-fax.de using the e-mail interface', metavar='DEST')
    parser.add_argument('--soap-simple-fax', help='Send a fax via simple-fax.de using the SOAP interface', metavar='DEST')
    parser.add_argument('--buy-stamp', help='Buy a stamp. Place postage file in current folder or use together with --adopt.', nargs='?', metavar='PRODUCT_ID', const='1')

    parser.add_argument('--lookup-address', help='Search for an address via Google. Can be used together with --adopt.', metavar='STRING')    
    parser.add_argument('--keep-folder', help='Store the adopted letter in the same folder', action='store_true')
    parser.add_argument('--config', help='The configuration file to use', default=config_file, metavar='FILE')   
    parser.add_argument('--verbose', help='Show what is going on', action='store_true')
    parser.add_argument('--configure', help='Initialize the environment and configure the tool', action='store_true')
    parser.add_argument('--version', help='Show version', action='store_true')
    
    (options, unknown_options) = parser.parse_known_args()

    if unknown_options:
        print("+ Unknown options: %s" % unknown_options)
        parser.print_help()
        
    
    if options.configure:

        old_config = None
        
        if os.path.exists(config_file):

            old_config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
            old_config.read([config_file])

        
        config = init_config_file(old_config)
        init_modules(config, old_config)

        with open(config_file, 'w') as cf_handle:
            print("+ Writing configuration file %s. You may want to edit this file later for further configuration." % config_file)
            config.write(cf_handle)
            os.chmod(config_file, 0o600)

        init_templates(config_file)            
                
        return
    elif options.version:
        print("+ Version: %s" % get_distribution("fensterbrief").version)
        return
        
    
    # create default config file?
    if not os.path.isfile(config_file):
        print("+ Can't find config file. Please run: %s --configure" % sys.argv[0])
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
        return
    
    if options.list_letters:
        fensterbrief.list_letters(root_dir)
        return

    if options.search:
        fensterbrief.list_letters(root_dir, options.search)
        return

    if options.set_folder:
        print("+ Set working folder to %s" % options.set_folder)
        fensterbrief.write_working_ref(root_dir, options.set_folder)
        return
        
    if options.create_folder:
        recipient_name = fensterbrief.request_recipient()
        foldername = fensterbrief.request_folder(recipient_name)
        dst_folder_path = fensterbrief.create_folder(root_dir, foldername)
        return

    if options.cat is not None:

        # abs or rel?           
        src_file = fensterbrief.expand_file_name(options.cat, root_dir)
           
        print("+ Print content of file %s" % src_file)

        fensterbrief.cat_file(src_file)
        return
    
    if options.lookup_address:
        fensterbrief.lookup_address(options.lookup_address, config)
            

    if options.adopt:
        address = None
        if options.lookup_address:
            address = fensterbrief.lookup_address(options.lookup_address, config)

        dst_file_name = fensterbrief.adopt(root_dir, options.adopt, options.keep_folder, address)

            
        if dst_file_name:
            if options.buy_stamp:
                f = frank.frank(config)
                f.buy_stamp(os.path.dirname(dst_file_name), options.buy_stamp)

            fensterbrief.edit_file(dst_file_name, config)

    if options.buy_stamp: # after adopt
        working_ref = fensterbrief.load_working_ref(root_dir)
        f = frank.frank(config)
        outdir = os.path.join(root_dir, working_ref['dir'])
        f.buy_stamp(outdir, options.buy_stamp)
        
    if options.edit is not None:

        if options.edit == '':
            working_ref = fensterbrief.load_working_ref(root_dir)
            src_file = os.path.join(root_dir, working_ref['dir'], working_ref['src'])
        else:
            # abs or rel?           
            src_file = fensterbrief.expand_file_name(options.edit, root_dir)
            
        print("+ Edit file %s" % src_file)

        # set working ref on edit
        fensterbrief.write_working_ref(root_dir, working_src_file=src_file)

        fensterbrief.edit_file(src_file, config)

        
    if options.render is not None:

        if options.render != '':
            src_file = fensterbrief.expand_file_name(options.render, root_dir)

            # set working ref on edit
            fensterbrief.write_working_ref(root_dir, working_src_file=src_file)
            
        working_ref = fensterbrief.load_working_ref(root_dir)
        src_file = os.path.join(root_dir, working_ref['dir'], working_ref['src'])
        pdf_file = os.path.join(root_dir, working_ref['dir'], working_ref['pdf'])

        print("+ Rendering file %s" % src_file)
        print("+ Output file %s" % pdf_file)

        
        if src_file.endswith('.tex'):
            fensterbrief.run_program(config['latex']['program'], ['-batch', src_file])
        elif src_file.endswith('.md'):
            fensterbrief.run_program(config['pandoc']['program'], \
                                     ['--template', config['pandoc']['template'], \
                                      '--output', pdf_file, src_file])
        else:
            print("+ Error: unknown file type for %s" % src_file)

    if options.show_pdf is not None:
        
        if options.show_pdf != '':
            pdf_file = fensterbrief.expand_file_name(options.show_pdf, root_dir)
        else:
            working_ref = fensterbrief.load_working_ref(root_dir)
            pdf_file = os.path.join(root_dir, working_ref['dir'], working_ref['pdf'])
        
        fensterbrief.run_program(config['DEFAULT']['pdf_viewer'], [pdf_file])

        
    if options.mail_simple_fax or options.soap_simple_fax:
      
        if options.mail_simple_fax:
            trans = mail_to_simple_fax_de.mail_to_simple_fax_de(config)
        else:
            trans = soap_to_simple_fax_de.soap_to_simple_fax_de(config)

        working_ref = fensterbrief.load_working_ref(root_dir)
        pdf_file = os.path.join(root_dir, working_ref['dir'], working_ref['pdf'])

        if options.mail_simple_fax:
            dst = options.mail_simple_fax
        else:
            dst = options.soap_simple_fax
            
        print("+ Going to send file: %s" % pdf_file)
        trans.send(pdf_file, dst, working_ref['pdf'])


        
if __name__ == "__main__":
    main()

