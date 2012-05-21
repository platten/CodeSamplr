"""config.py: Config file parser for codesamplr"""

import ConfigParser
import os


def return_config_dict(config_path):
    prefix = os.path.dirname(os.path.abspath(__file__))

    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(config_path)
    config_dict = {
        'VERBOSE': config.getboolean('General', 'verbose'),
        'ALLOW_FILETYPES': _parse_list(config.get('Filters',
                                                    'allow_filetypes')),
        'DISALLOWED_FILETYPES':  _parse_list(config.get('Filters',
                                                    'disallowed_filetypes')),
        'FILTER_FILENAMES': _parse_list(config.get('Filters',
                                                    'filter_filenames')),
        'ENCRYPT': config.getboolean('Encryption', 'encrypt'),
        'AUTHOR': config.get('Document', 'author'),
        'TITLE': config.get('Document', 'title'),
        'EMAIL': config.get('Document', 'email')
    }

    if config.get('Encryption', 'password'):
        config_dict['PASSWORD'] = config.get('Encryption', 'password')
    else:
        config_dict['PASSWORD'] = None

    if config.get('Paths', 'template_file'):
        config_dict['TEMPLATE'] = config.get('Paths', 'template_file')
    else:
        config_dict['TEMPLATE'] = os.path.join(prefix, 'template.tex')

    if config.get('Paths', 'highlight_path'):
        config_dict['HIGHLIGHT'] = config.get('Paths', 'highlight_path')
    else:
        config_dict['HIGHLIGHT'] = os.path.join(prefix, 'highlight.sty')

    for name, _ in config.items('Permissions'):
        config_dict['CAN_%s' % name.upper()] = config.getboolean('Permissions',
                                                                        name)

    return config_dict


def _parse_list(list_string):
    if not list_string:
        return None
    return list_string.split(',')
