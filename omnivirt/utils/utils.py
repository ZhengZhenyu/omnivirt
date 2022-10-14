import json
import os
import shutil
import subprocess
import sys
import yaml


def format_mac_addr(mac_str):
    ret = ''
    if len(mac_str) != 12:
        return ret
    mac_low = mac_str.lower()
    for i in range(0, 5):
        ret = ret + mac_low[2 * i] + mac_low[2 * i + 1] + '-'
    ret = ret + mac_low[-2] + mac_low[-1]
    
    return ret

def check_option(option, keyword):
    if not option:
        print('Should provide a valid %s!' % keyword)
        sys.exit(1)


def check_and_load_config(config_file):
    check_option(config_file, 'config file')

    with open(config_file, 'r') as config_file:
        config_options = yaml.load(config_file, Loader=yaml.SafeLoader)

    return config_options
