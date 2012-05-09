#!/usr/bin/env python

"""codesamplr.py: Convert sourcecode to encrypted PDFs with highlighted
                  syntax."""

__author__    = "Paul Pietkiewicz"
__copyright__ = "Copyright 2012, Paul Pietkiewicz"
__email__     = "pawel.pietkiewicz@acm.org"
__version__   = '0.888'

import os
import shutil
import sys
import argparse
from pprint import pprint
from functools import partial

from utils import *
from utils import convert_utils
from utils import file_utils

import config


def main():
    """CLI Driver"""
    parser = argparse.ArgumentParser(description='Source code to encrypted '
                                                 'PDF generator', \
                                     prog='codesamplr.py')

    parser.add_argument('sourceDirectory',
                        help='Directory containing source cdoe')
    parser.add_argument('-d', '--dest_format', dest='destination_path',
                        help='Destination directory')
    parser.add_argument('-f', '--footer', dest='footer',
        help='Footer (use for confidential message, etc.)\n '
             'NOTE: only works when using qt patched wkhtmltopdf',
        default='Confidential')
    #parser.add_argument('-c', '--config', dest='config_path', \
    #                    help='Path to alternate config file', action='store')
    parser.add_argument('-p', '--password', dest='password', \
                        help='Encryption password', action='store')
    parser.add_argument('-e', '--noencrypt', dest='encrypt',\
                        help='Disable PDF encryption', action='store_false')
    parser.add_argument('-v', '--verbose', dest='verbose',\
                        help='Verbose mode', action='store_true')

    cli_args = parser.parse_args()

    if 'destination_path' in cli_args and cli_args.destination_path:
        shutil.copytree(cli_args.sourceDirectory, cli_args.destination_path)
        delete = True
        file_list = directory_walker(cli_args.destination_path)

    else:
        delete = False
        file_list = directory_walker(cli_args.sourceDirectory)

    config.VERBOSE = cli_args.verbose
    file_utils.VERBOSE = cli_args.verbose
    convert_utils.VERBOSE = cli_args.verbose

    process = partial(processFile, delete=delete, encrypted=cli_args.encrypt,
                            password=cli_args.password, footer=cli_args.footer)

    for file in file_list:
        response = process(file)
        if config.VERBOSE:
            print "Source file type: %s" % file
            pprint(response)

    sys.exit(0)


def processFile(source_filepath, delete, encrypted, password, footer):
    html = return_HTML_highlighted_code(source_filepath)
    pdf = create_PDF(html, footer='bob')
    pdf_filepath = get_pdf_filename(source_filepath)
    response = write_PDF(pdf_filepath, pdf, encrypted=encrypted,
                    password=password)
    if delete:
        os.unlink(source_filepath)
    return response


if __name__ == "__main__":
    main()
    sys.exit(0)
