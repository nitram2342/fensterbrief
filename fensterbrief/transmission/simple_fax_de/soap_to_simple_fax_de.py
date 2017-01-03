from zeep import Client
import base64
import logging.config
import configparser

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

class mail_to_simple_fax_de:

    WSDLFILE = 'https://longisland.simple-fax.de/soap/index.php?wsdl'

    def __init__(self, config):
        self.config = config

    @staticmethod
    def init_config(config):
        config.set('soap_to_simple_fax_de', 'user', mail_from)
        config.set('soap_to_simple_fax_de', 'password', '')
        
    def send(self, file, dst_fax_nr, subject):

        client = Client(WSDLFILE)
        pdf_content = base64.b64encode(open(file, 'rb').read())

        user = self.config.get('soap_to_simple_fax_de', 'user')
        password = self.config.get('soap_to_simple_fax_de', 'password')

        result = client.service.sendfax(user, password, dst_fax_nr, pdf_content.decode("utf-8"), "PDF", "", "")

        print(result)
        return result
