# -*- coding: utf-8 -*-
#
#  Copyright 2016 Martin Schobert <martin@weltregierung.de>
#  

import configparser
import subprocess

class frank:

    def __init__(self, config):
        self.config = config

    @staticmethod
    def init_config(config):

        assert config != None
        
        config['frank'] = {}
        config['frank']['program'] = 'frank.py'
        config['frank']['product'] = '1'

    def buy_stamp(self, out_dir, product_id=None):
        
        program = self.config.get('frank', 'program')
        if product_id:
            product = product_id
        else:
            product = self.config.get('frank', 'product')

        print("+ Going to buy a stamp with product ID %s" % product)
        
        subprocess.call([program, '--format', '26', '--product', product,  '--output', out_dir, '";"'])

