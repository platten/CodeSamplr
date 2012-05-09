"""utils.py: File system related utilities functions for CodeSamplr"""

import sys
import os

from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

try:
    import codesamplr.config as config
except ImportError:
    import config

def should_open(filepath):
    """Check if should open file"""
    filename = os.path.split(filepath)[1]
    if os.path.isfile(filepath) and is_binary(filepath) or \
       filename in config.FILTER_FILENAMES or \
        (config.ALLOW_FILETYPES and
         os.path.splitext(filename)[1] not in config.ALLOW_FILETYPES) or \
        (config.DISALLOWED_FILETYPES and
         os.path.splitext(filename)[1] in config.ALLOW_FILETYPES):
        if config.VERBOSE:
            sys.stderr.write('IGNORING: %s\n' % filepath)
        return False
    try:
        get_lexer_for_filename(filepath)
    except ClassNotFound:
        if config.VERBOSE:
            sys.stderr.write('IGNORING: Lexer not found for %s\n' % filepath)
        return False
    if config.VERBOSE:
            sys.stdout.write('ADDING: %s\n' % filepath)
    return True


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


def directory_walker(root_dir):
    file_list = []
    root_dir = os.path.abspath(root_dir)
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            file_path = os.path.join(root, name)
            if should_open(file_path):
                file_list.append(file_path)
    return file_list


def get_pdf_filename(source_filepath):
    return source_filepath + '.pdf'
