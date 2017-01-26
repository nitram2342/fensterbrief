# -*- coding: utf-8 -*-
#
#  Copyright 2016 Martin Schobert <martin@weltregierung.de>
#  

import configparser
from fensterbrief import fensterbrief

def init_config(config, old_config):
        
    assert config != None
    
    fensterbrief.prompt("Your program for buying stamps via frank",
                        "frank", config, old_config, "frank", "program")
    
    fensterbrief.prompt("Your standard product when buying stamps via frank",
                        "1", config, old_config, "frank", "product")

    
class frank:

    def __init__(self, config):
        self.config = config


    def buy_stamp(self, out_dir, product_id=None):
        
        program = self.config.get('frank', 'program')
        if product_id:
            product = product_id
        else:
            product = self.config.get('frank', 'product')

        print("+ Going to buy a stamp with product ID %s" % product)
        
        fensterbrief.run_program(program, ['--format', '26', '--product', product,  '--output', out_dir, '";"'])

