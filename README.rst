Fensterbrief
============

``fensterbrief`` is a python script to organize and work with LaTeX-based letters.

----

Short introduction
==================

``fensterbrief`` (German for window envelope) is a helper script to manage the creation
and archival of LaTeX-based letters. It helps you in managing a folders in a structured
way and to name files in a consistent way. It helps in creating new letters based on
old ones. It tries to make letter writing easy witout adding over-specialised functionality.

``fensterbrief`` does not process metadata beyond file and directory names. It is not a
LaTeX editor.


Usage
-----

The ``fensterbrief`` tool is command line based: ::

    $ fensterbrief --help
    usage: fensterbrief [-h] [--config FILE] [--list-templates] [--list-letters]
                        [--search STRING] [--adopt FILE] [--init] [--keep-folder]
		        [--verbose] [--mail-simple-fax DEST]
			[--soap-simple-fax DEST]

    A command line tool to prepare letters
    
    optional arguments:
      -h, --help            show this help message and exit
      --config FILE         The configuration file to use
      --list-templates      List all letter templates
      --list-letters        List all letters
      --search STRING       Search for a string in filenames
      --adopt FILE          Create a new letter based on a previous one
      --init                Initialize the environment
      --keep-folder         Store the adopted letter in the same folder
      --verbose             Show what is going on
      --mail-simple-fax DEST
                            Send a fax via simple-fax.de using the e-mail
			    interface
      --soap-simple-fax DEST
                            Send a fax via simple-fax.de using the SOAP interface
							      

List all archived letters
-------------------------

::
  
    $ fensterbrief --list-letters
    + Looking up letters in /home/martin/Documents/Vorgaenge/
    [...]
    + 2010-09-company_X-anmeldung/2010-09-28_anmeldung.tex
    + 2010-09-company_X-anmeldung/2011-05-04-vertragsunterlagen.tex
    + 2014-09-company_Y-guthabenerstattung/2014-09-29-companyY-guthabenerstattung.tex
    [...]
    

Search for a string in directory and filenames
----------------------------------------------

::
   
    $ fensterbrief --search companyX
    + Looking up letters in /home/martin/Documents/Vorgaenge/
    [...]
    + 2010-09-company_X-anmeldung/2010-09-28_anmeldung.tex
    + 2010-09-company_X-anmeldung/2011-05-04-vertragsunterlagen.tex
    [...]

Create a new letter based on an old one
---------------------------------------

Often you already started a letter conversation with a recipient and have a followup letter. You like to adopt the old LaTeX letter, because you inserted reference numbers such as you customer or tax ID or the destination address. To write a new letter, you simply copy the old LaTeX file to a new destination folder. ::

     $ fensterbrief --adopt 2014-09-company_X-guthabenerstattung/2014-09-29-company_X-guthabenerstattung.tex
     Recipient short name: company X
     Folder subject: Klärung Situation X
     Letter subject: Klärung Situation X
     + Folder subject: Klarung_Situation_X
     + Letter subject: Klarung_Situation_X
     + Recipient: company_X
     + Creating folder /home/martin/Documents/Vorgaenge/2016-12_company_X-Klarung_Situation_X
     + Copy file /home/martin/Documents/Vorgaenge/2014-09-company_X-guthabenerstattung/2014-09-29-company_X-guthabenerstattung.tex to /home/martin/Documents/Vorgaenge/2016-12_company_X-Klarung_Situation_X/2016-12-14_company_X-Klarung_Situation_X.tex

Afterwards, the Fensterbrief script will launch the LaTeX editor that has been configured.

If you write a follow-up letter and want to store this letter in the same directory as the original letter, just add option --keep-folder. ::

     $ fensterbrief --adopt ... --keep-folder

When a letter is created, ``fensterbrief`` keeps track of it in a file ``${ROOT_DIR}/.working_object.conf``. This file references the current letter and simplifies the process of interacting with the letter.


Sending a letter
----------------

Usually, you will print your letter from the LaTex editor and close the editor afterwards. However, sometimes a letter should not be sent via snail mail, instead it should be sent via Fax. Because I use the prepaid service from http://simple-fax.de, ``fensterbrief`` supports this service provider.

Simple-fax.de supports fax sending via a `SOAP-based web API <http://simple-fax.de/Downloads/SOAP-API-simplefax.pdf>`_. However, this interface lacks support for a transmission confirmation. The simple-fax interface will call you back on your own web interface for status tracking, but you have to setup your status handler and you will not get a fancy transmission confirmation.

Therefore, I prefer the mail interface, because their e-mail interface sends status messages, a transmission confirmation PDF including the first page of your fax message, and you will have everything archived in your mail user agent. To send your letter ``fensterbrief`` will invoke your mail client. ::


     $ fensterbrief --mail-simple-fax <faxnum>

It will launch a prefilled 'new mail' dialog. Currently, only Thunderbird is supported. If you work with multiple e-mail accounts or e-mail identities, please make sure, the correct 'from' address is selected. The ``~/.fensterbrief.conf`` configuration file has a setting for this (``mail_from`` in section ``mail_to_simple_fax_de``). For some reason, an index such as ``id2`` must be specified to select the 'from' address instead of using just an ordinary e-mail address.


Buying postage
--------------

``Fensterbrief`` uses the tool ``frank``<https://github.com/gsauthof/frank> to buy stamps for the Deutsche Post. These stamps are named "Internetmarke" or "1C4A" for "1Click4Applikation". Once, ``frank`` is set up, you can buy stamps in two modes.

Buying postage, when creating a letter: ::

     $ fensterbrief --adopt 2014-09-company_X-guthabenerstattung/2014-09-29-company_X-guthabenerstattung.tex --buy-stamp

Buying postage for the current letter: ::

     $ fensterbrief --buy-stamp

The later approach works, because ``Fensterbrief`` stores the path and filenames of the current folder and letter.

     
Installation
==================

Technical installation of the tool itself
------------------------------------------

Clone the repository: ::

    $ git clone https://github.com/nitram2342/fensterbrief.git

Install the program: ::

    $ cd fensterbrief/
    $ sudo python3 setup.py install

Setup the environment 
---------------------

After installing the tool, the configuration file must be created. A wizzard mode asks for certain
configuration points as shown below. ::
   
    $ fensterbrief --init
    + Root directory, where letters should be stored: /home/martin/Documents/Vorgaenge/
    + Template directory, where template letters are stored: ${ROOT_DIR}/_templates/
    + Root directory, where letters should be stored: texmaker
    + Writing configuration file /home/martin/.fensterbrief.conf
    + Copy resource file to /home/martin/Documents/Vorgaenge//_templates/briefvorlage.lco
    + Copy resource file to /home/martin/Documents/Vorgaenge//_templates/template-widerspruch-datennutzung-nach-werbung.tex
    [...]
		    
It is possible to use text makros such as the ``${ROOT_DIR}``.

Customize templates
-------------------

The wizzard copys template files to the user's template directory. These templates should be
customized in a last step.

You can use your own LaTex templates. They can be based on the LaTeX g-brief, on scrlttr2 or on any other letter class. The templates that are shiped in this package are based on scrlttr2. There are plenty of template examples on the Internet, which you can adjust to your needs. My templates look like this:

* `Rendered standard letter template <./templates/template-standard-letter.pdf>`_
* `Rendered standard invoice template <./templates/template-invoice.pdf>`_
* `Rendered standard letter template for defeating advertising and personal data usage <./templates/template-widerspruch-datennutzung-nach-werbung.pdf>`_

When running ``--init``, ``.lco`` files are copied to the ``~/texmf/tex/latex/fensterbrief/`` directory and ``texhash`` is run afterwards.

Sample configuration file
-------------------------

Example configuration file ``~/.fensterbrief.conf``: ::

  [DEFAULT]
  root_dir = /home/martin/Documents/Vorgaenge/
  template_dir = ${ROOT_DIR}/_templates/
  editor = texmaker

  
  [mail_to_simple_fax_de]
  mail_client = thunderbird
  mail_from = id3

  
  [soap_to_simple_fax_de]
  user = foo@exmaple.com
  password = secret

  
  [frank]
  program = /home/martin/Development/frank/frank.py
  product = 1

Setup ``frank`` to buy stamps
-----------------------------

``Fensterbrief`` uses the tool ``frank`` to buy stamps, which itself is based on the python module [``python-inema``][https://pypi.python.org/pypi/inema].

Setting up ``frank`` is a bit complex, because it requires manual interactions aka. sending mails to the system operator. To use frank, please refer to the instructions on the `github page of ``frank```<https://github.com/gsauthof/frank>.

Create a signature file
-----------------------

Sometimes it is useful to have a digital version of one's signature to include it in a letter, when it is sent as fax via an Internet service. This is more convinient than printing a letter, placing a signature, scan it as PDF file.

A step-by-step guide to achieve this is describe in a `stackoverflow article`<https://tex.stackexchange.com/questions/32911/adding-a-signature-on-an-online-job-application/32940#32940>.
