import functools
import os
from threading import Thread
import json

from google.protobuf.json_format import MessageToDict

from omnivirt.utils import exceptions
from omnivirt.utils import objs


def asyncwrapper(fn):
    def wrapper(*args, **kwargs):
        thr = Thread(target=fn, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


def response2dict(fn):
    @functools.wraps(fn)
    def wrap(*args, **kwargs):
        response = fn(*args, **kwargs)
        response = MessageToDict(response)
        return response

    return wrap


def parse_config(args):
    if len(args) != 2 or args[0] != '--config-file':
        raise exceptions.NoConfigFileProvided
    if not os.path.exists(args[1]):
        raise exceptions.NoSuchFile(file=args[1])

    return objs.Conf(args[1])


def format_mac_addr(mac_str):
    ret = ''
    if len(mac_str) != 12:
        return ret
    mac_low = mac_str.lower()
    for i in range(0, 5):
        ret = ret + mac_low[2 * i] + mac_low[2 * i + 1] + '-'
    ret = ret + mac_low[-2] + mac_low[-1]
    
    return ret

def load_image_data(image_file):
    with open(image_file, 'r', encoding='utf-8') as fr:
            images = json.load(fr)['images']
        
    return images

def save_image_data(image_file, data):
    data_to_save = {
        'images': data
    }
    with open(image_file, 'w', encoding='utf-8') as fw:
            json.dump(data_to_save, fw, indent=4, ensure_ascii=False)
