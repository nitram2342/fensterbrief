""" The main routine for the fensterbrief script """

import argparse
import configparser
import subprocess
import os
from fensterbrief import fensterbrief

def main():

    # config
    config_file = os.path.expanduser('~/.fensterbrief.conf')

    # process command line arguments
    parser = argparse.ArgumentParser(description='A command line tool to prepare letters') 
    parser.add_argument('--config', help='The configuration file to use', default=config_file)
    parser.add_argument('--list-templates', help='List all letter templates', action='store_true')
    parser.add_argument('--list-letters', help='List all letters', action='store_true')
    parser.add_argument('--search', help='Search for a string in filenames')
    parser.add_argument('--adopt', help='Create a new letter based on a previous one')
    parser.add_argument('--show-path', help='Show full path for filenames', action='store_true')
    parser.add_argument('--verbose', help='Show what is going on', action='store_true')
      
    (options, args) = parser.parse_known_args()

    # create default config file?
    if not os.path.isfile(config_file):
        init_config_file(config_file)

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
        fensterbrief.list_letters(root_dir, options.show_path)

    elif options.search:
        fensterbrief.list_letters(root_dir, options.show_path, options.search)

    elif options.adopt:
        dst_file_name = fensterbrief.adopt(root_dir, options.adopt)
        subprocess.call([config.get('DEFAULT', 'EDITOR'), dst_file_name])
        
    else:
        print("+ Unknown option")
        parser.print_help()

        
if __name__ == "__main__":
    main()

