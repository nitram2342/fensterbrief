# -*- coding: utf-8 -*-
#
#  Copyright 2016 Martin Schobert <martin@weltregierung.de>
#  

from zeep import Client
import base64
import logging.config
import configparser

from fensterbrief import fensterbrief

logging.config.dictConfig({
        'version': 1,
        'formatters': {
                    'verbose': {
                                    'format': '%(name)s: %(message)s'
                                }
                },
        'handlers': {
                    'console': {
                                    'level': 'DEBUG',
                                    'class': 'logging.StreamHandler',
                                    'formatter': 'verbose',
                                },
                },
        'loggers': {
                    'zeep.transports': {
                                    'level': 'DEBUG',
                                    'propagate': True,
                                    'handlers': ['console'],
                                },
                }
    })

def init_config(config, old_config):

    assert config != None
    
    fensterbrief.prompt("Your e-mail address for simple-fax.de",
                        None, config, old_config, 'soap_to_simple_fax_de', 'user')
    
    fensterbrief.prompt("Your password for simple-fax.de (will be echoed)",
                        None, config, old_config, 'soap_to_simple_fax_de', 'password')
    

class soap_to_simple_fax_de:

    WSDLFILE = 'https://longisland.simple-fax.de/soap/index.php?wsdl'

    def __init__(self, config):
        self.config = config

        
    def send(self, file, dst_fax_nr, subject):

        client = Client(WSDLFILE)
        pdf_content = base64.b64encode(open(file, 'rb').read())

        user = self.config.get('soap_to_simple_fax_de', 'user')
        password = self.config.get('soap_to_simple_fax_de', 'password')

        result = client.service.sendfax(user, password, dst_fax_nr, pdf_content.decode("utf-8"), "PDF", "", "")

        print(result)
        return result
