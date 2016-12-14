Fensterbrief
============

Fensterbrief is a python script to organize and work with LaTeX-based letters.

----

Short introduction
==================

Fensterbrief (German for window envelope) is a helper script to manage the creation
and archival of LaTeX-based letters. It helps you creating directories in a structured
way and to name files in a consistent way. Fensterbrief does not process metadata
beyond file and directory names.


Usage
-----

The Fensterbrief tool is command line based:

    $ fensterbrief --help
    usage: fensterbrief [-h] [--config CONFIG] [--list-templates] [--list-letters]
                        [--search SEARCH] [--adopt ADOPT] [--show-path]
 		        [--verbose]
		       
    A command line tool to prepare letters
    
    optional arguments:
      -h, --help        show this help message and exit
      --config CONFIG   The configuration file to use
      --list-templates  List all letter templates
      --list-letters    List all letters
      --search SEARCH   Search for a string in filenames
      --adopt ADOPT     Create a new letter based on a previous one
      --show-path       Show full path for filenames
      --verbose         Show what is going on



List all archived letters:
------------


    $ fensterbrief --list-letters --show-path
    + Looking up letters in /home/martin/Documents/Vorgaenge/
    [...]
    + /home/martin/Documents/Vorgaenge/2010-09-company_X-anmeldung/2010-09-28_anmeldung.tex
    + /home/martin/Documents/Vorgaenge/2010-09-company_X-anmeldung/2011-05-04-vertragsunterlagen.tex
    + /home/martin/Documents/Vorgaenge/2014-09-company_Y-guthabenerstattung/2014-09-29-companyY-guthabenerstattung.tex
    [...]
    

Search for a string in directory and filenames
----------------------------------------------


    $ fensterbrief --search companyX --show-path
    + Looking up letters in /home/martin/Documents/Vorgaenge/
    [...]
    + /home/martin/Documents/Vorgaenge/2010-09-company_X-anmeldung/2010-09-28_anmeldung.tex
    + /home/martin/Documents/Vorgaenge/2010-09-company_X-anmeldung/2011-05-04-vertragsunterlagen.tex
    [...]

Create a new letter based on an old one
---------------------------------------

Often you already started a letter conversation with a recipient and have a followup letter. You like to adopt the old LaTeX letter, because you inserted reference numbers such as you customer or tax ID or the destination address. To write a new letter, you simply copy the old LaTeX file to a new destination folder.

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
    
Installation
==================

Technical installation of the tool itself
------------------------------------------



Setup the environment 
---------------------



Customize templates
-------------------






