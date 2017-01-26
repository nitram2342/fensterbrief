# -*- coding: utf-8 -*-
#
#  Copyright 2016 Martin Schobert <martin@weltregierung.de>
#  

import configparser
from fensterbrief import fensterbrief

def init_config(config, old_config=None):

    assert config != None

    fensterbrief.prompt("Your program for sending mail",
                        'thunderbird', config, old_config, 'mail_to_simple_fax_de', 'mail_client')
    
    fensterbrief.prompt("Your mail identity for sending mails to simple-fax.de",
                        'id1', config, old_config, 'mail_to_simple_fax_de', 'mail_from')

class mail_to_simple_fax_de:

    def __init__(self, config):
        self.config = config

        
    def send(self, file, dst_fax_nr, subject):
        
        mail_client = self.config.get('mail_to_simple_fax_de', 'mail_client')
        mail_from = self.config.get('mail_to_simple_fax_de', 'mail_from')

        if mail_client == 'thunderbird':
            mail = "preselectid=%s,to='%s@simple-fax.de',subject='%s',body='',attachment='%s'" % \
                   (mail_from, dst_fax_nr, subject, file)
            print(mail)
            fensterbrief.run_program(mail_client, ['-compose', mail ])

