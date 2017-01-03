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
        if res_name.endswith(".tex") or res_name.endswith(".lco"):
            src_fd = resource_stream('templates', res_name)            

            if res_name.endswith(".tex"):
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
    editor =       input("+ Your preferred LaTeX editor                           : ")

    config.set('DEFAULT', 'ROOT_DIR', root_dir)
    config.set('DEFAULT', 'TEMPLATE_DIR', template_dir)
    config.set('DEFAULT', 'EDITOR', editor)

    return config



def init_modules(config):
    mail_from = input("+ Your e-mail address for simple-fax.de                 : ")
    password =  input("+ Your password for simple-fax.de                       : ")
            
    mail_to_simple_fax_de.init_config(config)
    soap_to_simple_fax_de.init_config(config, mail_from, password)
    
    

def main():

    # config
    config_file = os.path.expanduser('~/.fensterbrief.conf')

    # process command line arguments
    parser = argparse.ArgumentParser(description='A command line tool to prepare letters') 
    parser.add_argument('--config', help='The configuration file to use', default=config_file, metavar='FILE')
    parser.add_argument('--list-templates', help='List all letter templates', action='store_true')
    parser.add_argument('--list-letters', help='List all letters', action='store_true')
    parser.add_argument('--create-folder', help='Ask for meta data and create a new folder', action='store_true')
    parser.add_argument('--search', help='Search for a string in filenames', metavar='STRING')
    parser.add_argument('--adopt', help='Create a new letter based on a previous one', metavar='FILE')
    parser.add_argument('--init', help='Initialize the environment', action='store_true')
    parser.add_argument('--keep-folder', help='Store the adopted letter in the same folder', action='store_true')
    parser.add_argument('--verbose', help='Show what is going on', action='store_true')
    parser.add_argument('--mail-simple-fax', help='Send a fax via simple-fax.de using the e-mail interface', metavar='DEST')
    parser.add_argument('--soap-simple-fax', help='Send a fax via simple-fax.de using the SOAP interface', metavar='DEST')
      
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
        fensterbrief.list_templates(template_dir)

    elif options.list_letters:
        fensterbrief.list_letters(root_dir)

    elif options.search:
        fensterbrief.list_letters(root_dir, options.search)

    elif options.create_folder:
        recipient_name = fensterbrief.request_recipient()
        foldername = fensterbrief.request_folder(recipient_name)
        dst_folder_path = fensterbrief.create_folder(root_dir, foldername)

    elif options.adopt:
        dst_file_name = fensterbrief.adopt(root_dir, options.adopt, options.keep_folder)
        subprocess.call([config.get('DEFAULT', 'EDITOR'), dst_file_name])

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

