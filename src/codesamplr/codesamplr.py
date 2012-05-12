#!/usr/bin/env python

"""codesamplr.py: Convert sourcecode to encrypted PDFs with highlighted
                  syntax."""

__author__    = "Paul Pietkiewicz"
__copyright__ = "Copyright 2012, Paul Pietkiewicz"
__email__     = "pawel.pietkiewicz@acm.org"
__version__   = '0.9'

import sys
import argparse
import os

from config import return_config_dict
from utils import prep_data, render_document, write_PDF


def main():
    """CLI Driver"""
    parser = argparse.ArgumentParser(description='Source code to encrypted '
                                                 'PDF generator', \
                                     prog='codesamplr.py')

    parser.add_argument('sourceDirectory',
                        help='Directory containing source cdoe')
    parser.add_argument('destination',
                        help='Destination')
    parser.add_argument('-c', '--config_file', dest='config_file',
        help='Config file')

    cli_args = parser.parse_args()

    if cli_args and cli_args.config_file:
        config = return_config_dict(cli_args.config_file)
    else:
        config = return_config_dict(os.path.join(os.path.dirname(
                                    os.path.abspath(__file__)),
                                    'codesamplr.cfg'))

    #TODO.markdown: add data prep error handling
    data_dict = prep_data(cli_args.sourceDirectory, config)
    tex_source = render_document(data_dict, config)
    #TODO.markdown: check if can write there
    write_PDF(cli_args.destination, tex_source, config)
    print "Done!"


if __name__ == "__main__":
    main()
    sys.exit(0)
