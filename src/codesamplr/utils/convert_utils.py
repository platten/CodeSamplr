"""convert_utils.py: Syntax highlighting and converting utility functions for CodeSamplr"""

from tempfile import mkstemp, NamedTemporaryFile
from random import choice
from string import digits, ascii_letters
from functools import partial

import os
import subprocess

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter

import config

def return_HTML_highlighted_code(filepath):
    """Return code as syntax highlighted HTML"""
    with open(filepath, 'r') as file_obj:
        lexer = get_lexer_for_filename(filepath)
        formatter = HtmlFormatter(style='colorful', linenos=True, full=True)#, cssclass="source")
        return highlight(file_obj.read(), lexer, formatter)


def reportlab_write_PDF(target_path, pdf_data, encrypted=True, password=''):
    if encrypted:
        if not password:
            password = _generate_password()
        temp_pdf = _write_PDF(pdf_data)
        encryptPdfOnDisk(
            temp_pdf,
            target_path,
            userPassword='',
            ownerPassword=password,
            canPrint=int(config.CAN_PRINT),
            canModify=int(config.CAN_MODIFY),
            canCopy=int(config.CAN_COPY),
            canAnnotate=int(config.CAN_ANNOTATE),
            strength=128)
        os.unlink(temp_pdf)
    else:
        _write_PDF(pdf_data, target_path)
    return {'path': target_path, 'password': password}

def _write_PDF(pdf_data, target_path=None):
    if not target_path:
        target_path = mkstemp(text=False)[1]
    with open(target_path, 'wb') as fb:
        fb.write(pdf_data)
    return target_path

def _generate_password(length=25):
    return ''.join([choice(digits + ascii_letters) for i in xrange(length)])

def pdktk_write_PDF(target_path, pdf_data, pdftk_path, encrypted=True, password=''):
    if encrypted:
        if not password:
            password = _generate_password()
        temp_pdf = _write_PDF(pdf_data)
        allow_list = []
        allow_dict = {'CAN_PRINT' : 'Printing',
                      'CAN_COPY': 'CopyContents',
                      'CAN_MODIFY': 'ModifyContents',
                      'CAN_ANNOTATE': 'ModifyAnnotations'}
        allow_list += [allow_dict[k] for k in allow_dict.keys() if getattr(config, k, False)]
        allow_str = 'allow %s' % ' '.join(allow_list)
        command = "%s A='%s' output '%s' %s encrypt_128bit owner_pw '%s'" % \
                                        (pdftk_path, temp_pdf, target_path,
                                        allow_str, password.encode('string-escape'))
        if config.VERBOSE:
            print command
        subprocess.check_call(command, shell=True)
        os.unlink(temp_pdf)
    else:
        _write_PDF(pdf_data, target_path)
    return {'path': target_path, 'password': password}


def convert_mac(html_content, footer=None):
    """Convert HTML to PDF using OSX's built in CUPS based PDF renderer"""
    temp_html_path = mkstemp(suffix='.html', text=True)[1]
    with open(temp_html_path, 'w') as fp:
        fp.write(html_content.encode('utf-8'))

    pdf =  subprocess.check_output('/System/Library/Printers/Libraries/convert -f "%s" 2>/dev/null' % temp_html_path, shell=True)
    os.unlink(temp_html_path)
    return pdf

def convert_wkhtmltopdf(html_content, wkhtmltopdf_path, footer):
    """Convert HTML to PDF using wkhtmltopdf Webkit based renderer"""
    # Bad idea to use this on mac, for some reason does not want to exit after conversion, works nice under linux though :)
    temp_html_path = mkstemp(suffix='.html', text=True)[1]
    with open(temp_html_path, 'w') as fp:
        fp.write(html_content)

    # Just get a filename, NamedTemporaryFile deletes after close by default
    temppdffile = NamedTemporaryFile(suffix='.pdf')
    temppdffile_path = temppdffile.name
    temppdffile.close()
    if footer:
        footer = '--footer-center "%s"' % footer
    else:
        footer = ''

    subprocess.check_call('%s -q %s %s %s' % (wkhtmltopdf_path, temp_html_path,
                                              footer, temppdffile_path), shell=True)
    with open(temppdffile_path, 'rb') as fp:
        pdf = fp.read()
    os.unlink(temppdffile_path)
    os.unlink(temp_html_path)
    return pdf

if not 'create_PDF' in globals():
    import platform

    if platform.system() == 'Darwin' and os.path.exists('/System/Library/Printers/Libraries/convert'):
        create_PDF = convert_mac
    else:
        wkhtmltopdf_path = subprocess.check_output('which wkhtmltopdf', shell=True).rstrip()
        create_PDF = partial(convert_wkhtmltopdf, wkhtmltopdf_path=wkhtmltopdf_path)

if not 'write_PDF' in globals():
    try:
        from reportlab.lib.pdfencrypt import encryptPdfOnDisk
        from rlextra.pageCatcher import pageCatcher
        write_PDF = reportlab_write_PDF
    except ImportError:
        pdftk_path = subprocess.check_output('which pdftk', shell=True).rstrip()
        write_PDF = partial(pdktk_write_PDF, pdftk_path=pdftk_path)
