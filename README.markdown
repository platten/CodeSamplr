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

Here is what it did: It used to keep your directory structure in tact and converts each file one by one to pdfs.

What it does now: it organizes everything in one nice big PDF.


Where:
-------
[https://github.com/platten/CodeSamplr](https://github.com/platten/CodeSamplr)


Prereqs:
--------
- Python 2.7
- [pygments](http://pygments.org/)
- [jinja2](http://jinja.pocoo.org/)
- [highlight](http://www.andre-simon.de/zip/download.html)
- [TexLive](http://www.tug.org/texlive/)
- [pdftk](http://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/)

Tested Installation on Ubuntu 10.04:
====================================
    sudo apt-get install git python-pygments python-jinja2 pdftk highlight texlive-full
    git clone http://github.com/platten/CodeSamplr
    cd CodeSamplr
    sudo python setup.py install


Licensing:
==========
See da LICENSE