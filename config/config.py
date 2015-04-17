#!/usr/bin/env python
# coding=utf-8
import os
import logging


homePath = os.path.dirname(os.path.realpath(__file__))
_config = {}
configPath = os.path.join(homePath, 'server.conf')
execfile(configPath, _config)

if not _config['log_path']:
    log_path = os.getcwd()
else:
    log_path = _config['log_path']
if not _config['log_level']:
    log_level = logging.WARNING
else:
    level_str = _config['log_level'].upper()
    if level_str.startswith('DEBUG'):
        log_level = logging.DEBUG
    if level_str.startswith('WARNING'):
        log_level = logging.WARNING
    if level_str.startswith('ERROR'):
        log_level = logging.ERROR
    
logging.basicConfig(\
    filename=os.path.join(log_path,'server.log'),\
    level=log_level)
