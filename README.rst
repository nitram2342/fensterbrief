``fensterbrief`` is a python script for working with letters based on LaTeX and
markdown.

.. contents:: 
   :local:

Short introduction
==================

``fensterbrief`` (German for window envelope) is a helper script to
manage the creation and archival of LaTeX- and Markdown-based
letters. It helps you in managing folders in a structured way and to
consistently name files. It helps in creating new letters based
on old ones. It tries to make letter writing easy witout adding
over-specialised functionality.

``fensterbrief`` does not process metadata beyond file and directory
names. It is not a LaTeX editor.

While ``fensterbrief`` is more or less OS independent, it currently only
supports Unix-style environments.

Features
--------

-  intended to be used via command line
-  maintaining a folder and document structure
-  support for LaTeX and Markdown based letters
-  support for fax transmissions via simple-fax.de
-  support for buying postage for the Deutsche Post
-  lookup postal addresses via the Google API

Usage
-----

The ``fensterbrief`` tool is command line based:

::

        $ fensterbrief --help
	usage: fensterbrief [-h] [--list-templates] [--list-letters] [--search STRING]
                    [--create-folder] [--adopt FILE] [--edit [FILE]]
                    [--render [FILE]] [--show-pdf [FILE]] [--set-folder DIR]
                    [--cat FILE] [--mail-simple-fax DEST]
                    [--soap-simple-fax DEST] [--buy-stamp [PRODUCT_ID]]
                    [--lookup-address STRING] [--keep-folder] [--config FILE]
                    [--verbose] [--configure] [--version]

        Manage letters via command line

        optional arguments:
	  -h, --help            show this help message and exit
	  --list-templates      List all letter templates
	  --list-letters        List all letters
	  --search STRING       Search for a string in filenames
	  --create-folder       Ask for meta data and create a new folder
	  --adopt FILE          Create a new letter based on a previous one
	  --edit [FILE]         Edit the current letter or another source file
	  --render [FILE]       Render PDF file from current markdown or latex
	  --show-pdf [FILE]     Open PDF file in PDF viewer
	  --set-folder DIR      Set the working folder
	  --cat FILE            Dump content of a letter
	  --mail-simple-fax DEST
                                Send a fax via simple-fax.de using the e-mail
                                interface
	  --soap-simple-fax DEST
                                Send a fax via simple-fax.de using the SOAP interface
	  --buy-stamp [PRODUCT_ID]
                                Buy a stamp. Place postage file in current folder or
				use together with --adopt.
          --lookup-address STRING
                                Search for an address via Google. Can be used together
                                with --adopt.
	  --keep-folder         Store the adopted letter in the same folder
	  --config FILE         The configuration file to use
	  --verbose             Show what is going on
	  --configure           Initialize the environment and configure the tool
	  --version             Show version



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

Often you already started a letter conversation with a recipient and
have a followup letter. You like to adopt the old LaTeX letter, because
you inserted reference numbers such as you customer or tax ID or the
destination address. To write a new letter, you simply copy the old
LaTeX file to a new destination folder. Technically, it makes no
difference, whether you adopt an old letter or a template file.

::

         $ fensterbrief --adopt 2014-09-company_X-guthabenerstattung/2014-09-29-company_X-guthabenerstattung.tex
         Recipient short name: company X
         Folder subject: Klärung Situation X
         Letter subject: Klärung Situation X
         + Folder subject: Klarung_Situation_X
         + Letter subject: Klarung_Situation_X
         + Recipient: company_X
         + Creating folder /home/martin/Documents/Vorgaenge/2016-12_company_X-Klarung_Situation_X
         + Copy file /home/martin/Documents/Vorgaenge/2014-09-company_X-guthabenerstattung/2014-09-29-company_X-guthabenerstattung.tex to /home/martin/Documents/Vorgaenge/2016-12_company_X-Klarung_Situation_X/2016-12-14_company_X-Klarung_Situation_X.tex

Afterwards, the fensterbrief script will launch the LaTeX editor that
has been configured. Since LaTeX editors usually support a build-in
function for rendering and printing, there are no further steps relevant
here. If you use a editor that does not support rendering, you can
render your letter from command line, too. Please refer to the bext
section.

If you write a follow-up letter and want to store this letter in the
same directory as the original letter, just add option --keep-folder.

::

         $ fensterbrief --adopt ... --keep-folder

When a letter is created, ``fensterbrief`` keeps track of it in a file
``${ROOT_DIR}/.working_object.conf``. This file references the current
letter and simplifies the process of interacting with the letter.

Markdown-based letters
----------------------

Adopting a Markdown letter isn't much different from creating a
LaTeX-based letter. The source file of a Markdown-based letter looks
like this:

`Sample Markdown letter <https://github.com/nitram2342/fensterbrief/templates/template-pandoc.md>`__

Usually, you likely use a more general editor that may not support
LaTeX/pandoc directly. Therefore, you may want to render your letters
explicitly as shown below:

::

         $ fensterbrief --render

Afterwards you can open the rendered PDF file in a PDF viewer, check the
output and print the document:

::

         $ fensterbrief --show-pdf


If you want to make further changes to your letter, you can run the
editor again:

::

         $ fensterbrief --edit


Commands can be chained, for example:

::

         $ fensterbrief --edit --render --show-pdf


To render PDF files from Markdown via LaTeX, ``fensterbrief`` uses
`pandoc <https://pandoc.org/>`__ with this LaTeX template:

`LaTeX letter template used as pandoc
template <https://github.com/nitram2342/fensterbrief/templates/template-pandoc.tex>`__

Sending a letter
----------------

Usually, you will print your letter from the LaTex editor and close the
editor afterwards. However, sometimes a letter should not be sent via
snail mail, instead it should be sent via Fax. Because I use the prepaid
service from http://simple-fax.de, ``fensterbrief`` supports this
service provider.

Simple-fax.de supports fax sending via a `SOAP-based web
API <http://simple-fax.de/Downloads/SOAP-API-simplefax.pdf>`__. However,
this interface lacks support for a transmission confirmation. The
simple-fax interface will call you back on your own web interface for
status tracking, but you have to setup your status handler and you will
not get a fancy transmission confirmation.

Therefore, I prefer the mail interface, because their e-mail interface
sends status messages, a transmission confirmation PDF including the
first page of your fax message, and you will have everything archived in
your mail user agent. To send your letter ``fensterbrief`` will invoke
your mail client.

::

         $ fensterbrief --mail-simple-fax <faxnum>

It will launch a prefilled 'new mail' dialog. Currently, only
Thunderbird is supported. If you work with multiple e-mail accounts or
e-mail identities, please make sure, the correct 'from' address is
selected. The ``~/.fensterbrief.conf`` configuration file has a setting
for this (``mail_from`` in section ``mail_to_simple_fax_de``). For some
reason, an index such as ``id2`` must be specified to select the 'from'
address instead of using just an ordinary e-mail address.

Buying postage
--------------

``fensterbrief`` uses the tool
`frank <https://github.com/gsauthof/frank>`__ to buy stamps for the
Deutsche Post. These stamps are named "Internetmarke" or "1C4A" for
"1Click4Applikation". Once, ``frank`` is set up, you can buy stamps in
two modes.

Buying postage, when creating a letter:

::

         $ fensterbrief --adopt 2014-09-company_X-guthabenerstattung/2014-09-29-company_X-guthabenerstattung.tex --buy-stamp

Buying postage for the current letter:

::

         $ fensterbrief --buy-stamp

The later approach works, because ``fensterbrief`` stores the path and
filenames of the current folder and letter.

Lookup an address
-----------------

When adopting a Markdown-based letter, you can lookup a postal address
via Google and the address is used in the letter as destination address:

::

    $ fensterbrief --adopt _templates/template-pandoc.md --keep-folder --lookup-address 'rathaus mitte, berlin'

If there are multiple matches, a list of matches is shown and you select
an index.

This operation requires a Google API key.

Installation
============

Technical installation of the tool itself
-----------------------------------------

Install dependencies:

::

        $ sudo apt-get install texlive texlive-lang-german \
	    texlive-fonts-extra texlive-latex-extra texlive-generic-recommended \
	    python3-pip pandoc \
	     

Install ``fensterbrief``:

::

        $ sudo pip3 install fensterbrief
	

Setup the environment
---------------------

After installing the tool, the configuration file must be created. A
wizzard mode asks for certain configuration points as shown below.

::

 $ fensterbrief --configure
 + Root directory, where letters should be stored
   ---------------------------------------------------------------
   Default value: /home/martin/Documents/letters/
   Current value: /home/martin/Documents/Vorgaenge/
   Enter: keep current configuration, 'd': use default configuration
   > 
 + Use value: /home/martin/Documents/Vorgaenge/

 + Template directory, where template letters are stored
   ---------------------------------------------------------------
   Default value: ${ROOT_DIR}/_templates/
   Current value: /home/martin/Documents/Vorgaenge//_templates/
   Enter: keep current configuration, 'd': use default configuration
   > d
 + Use value: ${ROOT_DIR}/_templates/

   [...]

It is possible to use text makros such as the ``${ROOT_DIR}``.



Update the installation
-----------------------

To upgrade ``fensterbrief``, use the following commands:

::

        $ sudo pip3 install fensterbrief --upgrade
	$ fensterbrief --configure
	
If ``--configure`` is used and there is already a configuration file, ``fensterbrief`` will ask whether you want to use the default value or an existing configuration entry or a new value.


Customize templates
-------------------

The wizzard copys template files to the user's template directory. These
templates should be customized in a last step.

You can use your own LaTeX templates. They can be based on the LaTeX
g-brief, on scrlttr2 or on any other letter class. The templates that
are shipped in this package are based on scrlttr2. There are plenty of
template examples on the Internet, which you can adjust to your needs.
My templates look like this:

-  `Rendered standard letter
   template <https://github.com/nitram2342/fensterbrief/templates/template-standard-letter.pdf>`__
-  `Rendered standard invoice
   template <https://github.com/nitram2342/fensterbrief/templates/template-invoice.pdf>`__
-  `Rendered standard letter template for defeating advertising and
   personal data
   usage <https://github.com/nitram2342/fensterbrief/templates/template-widerspruch-datennutzung-nach-werbung.pdf>`__

When running ``--configure``, ``.lco`` files are copied to the
``~/texmf/tex/latex/fensterbrief/`` directory and ``texhash`` is run
afterwards.

Sample configuration file
-------------------------

Example configuration file ``~/.fensterbrief.conf``:

::

      [DEFAULT]
      root_dir = /home/martin/Documents/Vorgaenge/
      template_dir = ${ROOT_DIR}/_templates/
      tex_editor = texmaker
      md_editor = emacs -nw
      
      [pandoc]
      program = pandoc
      template = ${template_dir}/template-pandoc.tex
      
      [latex]
      program = latex
      
      [google]
      api_key = xxxx
      
      [mail_to_simple_fax_de]
      mail_client = thunderbird
      mail_from = id3
      
      [soap_to_simple_fax_de]
      user = foo@example.com
      password = secret
      
      [frank]
      program = /home/martin/Development/frank/frank.py
      product = 1

Setup ``frank`` to buy stamps
-----------------------------

``fensterbrief`` uses the tool ``frank`` to buy stamps, which itself is
based on the python module
`python-inema <https://pypi.python.org/pypi/inema>`__.

Setting up ``frank`` is a bit complex, because it requires manual
interactions aka. sending mails to the system operator. To use frank,
please refer to the instructions on the `github page of
frank <https://github.com/gsauthof/frank>`__.

Create a signature file
-----------------------

Sometimes it is useful to have a digital version of one's signature to
include it in a letter, when it is sent as fax via an Internet service.
This is more convinient than printing a letter, placing a signature,
scan it as PDF file.

A step-by-step guide to achieve this is describe in a `stackoverflow
article <https://tex.stackexchange.com/questions/32911/adding-a-signature-on-an-online-job-application/32940#32940>`__.

Obtain a Google API key
-----------------------

You need a Google API key in order to use this feature. You can get an
API key from
`Google <https://developers.google.com/maps/documentation/javascript/get-api-key>`__,
which requires a Google account.

It may also be possible to find API keys at
`Github <https://github.com/search?o=desc&q=google+maps+api+key&ref=searchresults&s=indexed&type=Code>`__

Copyright and Licence
=====================

``fensterbrief`` is developed by Martin Schobert martin@schobert.cc and
published under a BSD licence with a non-military clause. Please read
``LICENSE.txt`` for further details.
