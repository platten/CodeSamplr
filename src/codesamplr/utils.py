"""utils.py: Syntax highlighting and converting utility functions
                    for CodeSamplr"""

from tempfile import NamedTemporaryFile, mkstemp
from random import choice
from string import digits, ascii_letters

import sys
import os
import subprocess

from jinja2 import Template
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

id_list = []


#
# Supplemental functions
#
def _generate_password(length=25):
    return ''.join([choice(digits + ascii_letters) for i in xrange(length)])


def is_binary(filename):
    """Return true if the given filename is binary.
    @raise EnvironmentError: if the file does not exist or cannot be accessed.
    @author: Trent Mick <TrentM@ActiveState.com>
    @author: Jorge Orpinel <jorge@orpinel.com>"""
    fin = open(filename, 'rb')
    try:
        CHUNKSIZE = 1024
        while 1:
            chunk = fin.read(CHUNKSIZE)
            if '\0' in chunk:  # found null byte
                return True
            if len(chunk) < CHUNKSIZE:
                break  # done
    finally:
        fin.close()
    return False


def random_id(length=50):
    global id_list
    new_id = ''.join([choice(ascii_letters) for i in xrange(length)])

    while new_id in id_list:
        new_id = ''.join([choice(ascii_letters) for i in xrange(length)])

    id_list.append(new_id)
    return new_id

#
# Data conversion
#
def get_tex_syntax(path):
    highlight_path = subprocess.check_output('which highlight',
        shell=True).rstrip()

    #TODO.markdown: this unicode stuff should be cleaned up
    content = unicode(subprocess.check_output('%s --style solarized-light -O '
                                  'latex --pretty-symbols -l  -f "%s"' % \
                                (highlight_path, path), shell=True), 'utf-8')
    return content


def write_PDF(pdf_destination, tex_source, config):
    if config['ENCRYPT']:
        pdftk_path = subprocess.check_output('which pdftk',
            shell=True).rstrip()
        if not config['PASSWORD']:
            password = _generate_password()
        else:
            password = config['PASSWORD']
        temp_pdf = convert_tex(tex_source, config)
        allow_list = []
        allow_dict = {'CAN_PRINT': 'Printing',
                      'CAN_COPY': 'CopyContents',
                      'CAN_MODIFY': 'ModifyContents',
                      'CAN_ANNOTATE': 'ModifyAnnotations'}
        allow_list += [allow_dict[k] for k in allow_dict.keys()
                       if getattr(config, k, False)]
        allow_str = 'allow %s' % ' '.join(allow_list)
        command = "%s A='%s' output '%s' %s encrypt_128bit owner_pw '%s'" % \
                                (pdftk_path, temp_pdf, pdf_destination,
                                 allow_str, password.encode('string-escape'))
        if config['VERBOSE']:
            print command
        subprocess.check_call(command, shell=True)
        os.unlink(temp_pdf)
    else:
        password = None
        convert_tex(tex_source, config, pdf_destination)
    return {'path': pdf_destination, 'password': password}


def convert_tex(tex_source, config, pdf_destination=None):
    if not pdf_destination:
        pdf_destination = mkstemp(suffix='.pdf')[1]

    tex_temp = NamedTemporaryFile(mode='w', suffix='.tex', delete=False)
    tex_temp.write(tex_source.encode('utf-8'))
    tex_temp_path = tex_temp.name
    tex_temp.close()

    command = "texi2pdf -c -s --output='%s' '%s'" %\
              (pdf_destination, tex_temp_path)
    if config['VERBOSE']:
        print command
    subprocess.check_call(command, shell=True)
    os.unlink(tex_temp_path)
    return pdf_destination


def render_document(data_dict, config):
    with open(config['TEMPLATE'], 'r') as fp:
        tex_template = fp.read()
    template = Template(tex_template)
    return template.render(data_dict)


#
# File handling
#
def should_open(filepath, config):
    """Check if should open file"""
    filename = os.path.split(filepath)[1]
    if os.path.isfile(filepath) and is_binary(filepath) or\
       filename in config['FILTER_FILENAMES'] or\
       (config['ALLOW_FILETYPES'] and
        os.path.splitext(filename)[1] not in config['ALLOW_FILETYPES']) or\
       (config['DISALLOWED_FILETYPES'] and
        os.path.splitext(filename)[1] in config['DISALLOWED_FILETYPES']):
        if config['VERBOSE']:
            sys.stderr.write('IGNORING: %s\n' % filepath)
        return False
    try:
        #TODO.markdown: find better way to find if language is supported
        get_lexer_for_filename(filepath)
    except ClassNotFound:
        if config['VERBOSE']:
            sys.stderr.write('IGNORING: Lexer not found for %s\n' % filepath)
        return False
    if config['VERBOSE']:
        sys.stdout.write('ADDING: %s\n' % filepath)
    return True


def directory_walker(root_dir, config):
    file_list = []
    tree_list = ["\dirtree{%", ".1 root."]
    root_dir = os.path.abspath(root_dir)
    level = 2
    dirname = os.path.basename(os.path.dirname(root_dir))
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            file_path = os.path.join(root, name)
            if should_open(file_path, config):
                this_level = get_level(file_path, root_dir)
                if this_level != level or \
                   os.path.basename(os.path.dirname(file_path)) != dirname:
                    level = this_level
                    dirname = os.path.basename(os.path.dirname(file_path))
                    tree_list.append('.' + str(this_level - 1) +
                                     ' ' + escape_latex(dirname) + '.')
                try:
                    temp_dict = {'safename': escape_latex(os.path.basename(
                                                                file_path)),
                                 'hash': random_id(),
                                 'texcontent': get_tex_syntax(file_path)}
                except Exception as e:
                    sys.stderr.write('Exception "%s" in file %s\n' %
                                                        (str(e), file_path))
                    continue
                tree_list.append(".%d \hyperref[%s]{%s}." % (this_level,
                                                        temp_dict['hash'],
                                                        temp_dict['safename']))
                file_list.append(temp_dict)
    tree_list.append('}')
    return file_list, "\n".join(tree_list)


def get_level(path, root_dir):
    return len(os.path.relpath(path, root_dir).split('/')) + 1


def prep_data(path, config):
    file_list, tree = directory_walker(path, config)
    return {'author': escape_latex(config['AUTHOR']),
            'title': escape_latex(config['TITLE']),
            'highlight_path': escape_latex(config['HIGHLIGHT']),
            'tree': tree,
            'syntaxfiles': file_list}

#
# Taken from Volker Grabsch's tex module
# http://packages.python.org/tex/
#
_latex_special_chars = {
	u'$':  u'\\$',
	u'%':  u'\\%',
	u'&':  u'\\&',
	u'#':  u'\\#',
	u'_':  u'\\_',
	u'{':  u'\\{',
	u'}':  u'\\}',
	u'[':  u'{[}',
	u']':  u'{]}',
	u'"':  u"{''}",
	u'\\': u'\\textbackslash{}',
	u'~':  u'\\textasciitilde{}',
	u'<':  u'\\textless{}',
	u'>':  u'\\textgreater{}',
	u'^':  u'\\textasciicircum{}',
	u'`':  u'{}`',   # avoid ?` and !`
	u'\n': u'\\\\',
}

def escape_latex(s):
	r'''Escape a unicode string for LaTeX.

	:Warning:
	  The source string must not contain empty lines such as:
	      - u'\n...' -- empty first line
	      - u'...\n\n...' -- empty line in between
	      - u'...\n' -- empty last line

	:Parameters:
	  - `s`: unicode object to escape for LaTeX

	>>> s = u'\\"{}_&%a$b#\nc[]"~<>^`\\'
	>>> escape_latex(s)
	u"\\textbackslash{}{''}\\{\\}\\_\\&\\%a\\$b\\#\\\\c{[}{]}{''}\\textasciitilde{}\\textless{}\\textgreater{}\\textasciicircum{}{}`\\textbackslash{}"
	>>> print s
	\"{}_&%a$b#
	c[]"~<>^`\
	>>> print escape_latex(s)
	\textbackslash{}{''}\{\}\_\&\%a\$b\#\\c{[}{]}{''}\textasciitilde{}\textless{}\textgreater{}\textasciicircum{}{}`\textbackslash{}
	'''
	return u''.join(_latex_special_chars.get(c, c) for c in s)