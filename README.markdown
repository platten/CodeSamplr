CodeSamplr
==========
<i>Paul Pietkiewicz <paul.pietkiewicz at acm dot org> </i>


Intro:
-------

Alright, so you're looking for a job. Not just any job, THE JOB. Got the checklist right here:

- Resume: check
- Cover letter: check
- Sample code?

Uhm, yeah that.

So you have some sample code. You wrote it here or there, and you want to show it. But… you don't want someone to use it easily.

So you can print it out and take it to your interview. You can take pictures of it and send them.

Or you could have the file packaged up in an syntax highlighted encrypted PDF.

That what this does. Yes, it keeps your directory structure in tact and converts each file one by one to pdfs. No it doesn't organize everything in one nice big PDF, but its a start.


Where:
-------
[https://github.com/platten/CodeSamplr](https://github.com/platten/CodeSamplr)


Prereqs:
--------
- Python 2.7
- [pygments](http://pygments.org/)

-  A PDF generating library like [wkhtmltopdf](https://code.google.com/p/wkhtmltopdf/) (or [reportlab](https://www.reportlab.com/software/))
- Something for PDF Encryption like [pdftk](http://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/) (or [reportlab w/ rlextras](https://www.reportlab.com/software/installation/))


Tested Installation on Ubuntu 10.04:
====================================
    sudo apt-get install git python-pygments pdftk wkhtmltopdf
    git clone http://github.com/platten/CodeSamplr
    cd CodeSamplr
    sudo python setup.py install


Licensing:
==========
See da LICENSE