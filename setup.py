#!/usr/bin/env python

from distutils.core import setup
import sys
import glob

sys.path.append('./src')
from codesamplr.codesamplr import __version__ as codesamplr_version

setup(
    name = 'CodeSamplr',
    author       = 'Paul Pietkiewicz',
    author_email = 'pawel.pietkiewicz@acm.org',
    description  = 'Convert sourcecode into encrypted PDFs with highlighted syntax',
    license      = 'PSF',
    keywords     = 'encrypt pdf syntax highlight',
    url          = 'https://github.com/platten/CodeSamplr/',

    version          = codesamplr_version,
    install_requires = ['pygments'],
	packages         = ['codesamplr', 'codesamplr.utils'],
	package_dir      = {'codesamplr': 'src/codesamplr','codesamplr.utils': 'src/codesamplr/utils'},
    scripts          = glob.glob("bin/*")
)


