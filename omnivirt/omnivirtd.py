import json
import os
import sys
import wget
import lzma
import shutil
import time

from omnivirt import vmops
from omnivirt.utils import utils
from omnivirt import constants


CONFIG_FILE = 'D:\\omnivirt\\etc\\conf.yaml'

config_options = utils.check_and_load_config(CONFIG_FILE)

work_dir = config_options['work_dir']
image_dir = work_dir + constants.IMG_DIR
img_record_file = os.path.join(image_dir, 'images.json')
instance_dir = os.path.join(work_dir, 'instances')


def init(args):
    if len(args) != 2 or args[0] != '--config-file':
        raise 
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    if not os.path.exists(img_record_file):
        image_body = {
            'images': []
        }
        with open(img_record_file, 'w', encoding='utf-8') as fw:
            json.dump(image_body, fw, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    init(sys.argv[1:])
    serve()
