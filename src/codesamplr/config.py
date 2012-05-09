"""config.py: Config file for codesamplr"""


import os
from string import Template

VERBOSE = False

# Ensure that only files with the following file types are converted
ALLOW_FILETYPES = ['.py']

# Ensure that files with the following file types are ignored
DISALLOWED_FILETYPES = []

# Filter out the following files
FILTER_FILENAMES=['__init__.py']

CAN_COPY=False
CAN_PRINT=False
CAN_MODIFY=False
CAN_ANNOTATE=False