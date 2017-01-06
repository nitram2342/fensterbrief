# -*- coding: utf-8 -*-
#
#  Copyright 2016 Martin Schobert <martin@weltregierung.de>
#  

import configparser
import subprocess

class mail_to_simple_fax_de:

    def __init__(self, config):
        self.config = config

    @staticmethod
    def init_config(config):

        assert config != None

        config['mail_to_simple_fax_de'] = {}        
        config['mail_to_simple_fax_de']['mail_client'] = 'thunderbird'
        config['mail_to_simple_fax_de']['mail_from'] = 'id1'
        
        
    def send(self, file, dst_fax_nr, subject):
        
        mail_client = self.config.get('mail_to_simple_fax_de', 'mail_client')
        mail_from = self.config.get('mail_to_simple_fax_de', 'mail_from')

        if mail_client == 'thunderbird':
            mail = "preselectid=%s,to='%s@simple-fax.de',subject='%s',body='',attachment='%s'" % \
                   (mail_from, dst_fax_nr, subject, file)
            print(mail)
            subprocess.call([mail_client, '-compose', mail ])

