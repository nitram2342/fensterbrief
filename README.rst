Fensterbrief
============

Fensterbrief is a python script to organize and work with LaTeX-based letters.

----

Short introduction
==================

Fensterbrief (German for window envelope) is a helper script to manage the creation
and archival of LaTeX-based letters. It helps you in managing a folders in a structured
way and to name files in a consistent way. It helps in creating new letters based on
old ones. It tries to make letter writing easy witout adding over-specialised functionality.

Fensterbrief does not process metadata beyond file and directory names. It is not a
LaTeX editor.


Usage
-----

The Fensterbrief tool is command line based: ::

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
							      

List all archived letters:
------------

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

     $ fensterbrief --adopt /home/martin/Documents/Vorgaenge/2014-09-company_X-guthabenerstattung/2014-09-29-company_X-guthabenerstattung.tex
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
		    
It is possible to use text makros such as the ${ROOT_DIR}.

Customize templates
-------------------

The wizzard copys template files to the user's template directory. These templates should be
customized in a last step.

You can use your own LaTex templates. They can be based on the LaTeX g-brief, on scrlttr2 or on any other letter class. The templates that are shiped in this package are based on scrlttr2. There are plenty of template examples on the Internet, which you can adjust to your needs. My templates look like this:

* `Rendered standard letter template <./templates/template-standard-letter.pdf>`_
* `Rendered standard invoice template <./templates/template-invoice.pdf>`_
* `Rendered standard letter template for defeating advertising and personal data usage <./templates/template-widerspruch-datennutzung-nach-werbung.pdf>`_

When running ``--init``, ``.lco`` files are copied to the ``~/texmf/tex/latex/fensterbrief/`` directory and ``texhash`` is run afterwards.

