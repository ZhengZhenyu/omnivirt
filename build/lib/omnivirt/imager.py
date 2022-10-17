import json
import os
import wget
import lzma

from omnivirt.utils import utils
from omnivirt.utils import constants
from omnivirt.utils import powershell

CONFIG_FILE = 'D:\\omnivirt\\etc\\conf.yaml'

config_options = utils.check_and_load_config(CONFIG_FILE)

work_dir = config_options['work_dir']
image_dir = work_dir + constants.IMG_DIR
img_record_file = os.path.join(image_dir, 'images.json')
instance_dir = os.path.join(work_dir, 'instances')


def download_image(image_id):
    try:
        image_url = constants.OPENEULER_IMGS[image_id]
    except KeyError:
        raise

    # Download the image
    img_name = wget.filename_from_url(image_url)
    if not os.path.exists(os.path.join(image_dir, img_name)):
        print('Downloading image from remote repo, this might take a while ...\n')
        wget.download(url=image_url, out=os.path.join(image_dir, img_name))
    
    # Decompress the image
    print('Decompressing image ...\n')
    qcow2_name = img_name[:-3]
    with open(os.path.join(image_dir, img_name), 'rb') as pr, open(os.path.join(image_dir, qcow2_name), 'wb') as pw:
        data = pr.read()
        data_dec = lzma.decompress(data)
        pw.write(data_dec)
    
    # Convert the qcow2 img to vhdx
    vhdx_name = image_id + '.vhdx'
    print('Converting image ...\n')
    with powershell.PowerShell('GBK') as ps:
        cmd = 'qemu-img convert -O vhdx {0} {1}'
        outs, errs = ps.run(cmd.format(os.path.join(image_dir, qcow2_name), os.path.join(image_dir, vhdx_name)))
    
    # Record local image
    with open(img_record_file, 'r', encoding='utf-8') as fr:
        local_images = json.load(fr)['images']
    
    image_info = {
        'image_id': image_id,
        'image_path': os.path.join(image_dir, vhdx_name)
    }

    found = False
    for img in local_images:
        if img['image_id'] == image_id:
            img['image_path'] = image_info['image_path']
            found = True
            break
    
    if not found:
        local_images.append(image_info)
    
    image_body = {
            'images': local_images
        }
    with open(img_record_file, 'w', encoding='utf-8') as fw:
        json.dump(image_body, fw, indent=4, ensure_ascii=False)

    # TODO: Cleanup temp images?
    pass