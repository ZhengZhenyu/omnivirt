import copy
import lzma
import wget
import os
import ssl

from omnivirt.backends.win import powershell
from omnivirt.utils import constants
from omnivirt.utils import utils as omni_utils


ssl._create_default_https_context = ssl._create_unverified_context


class WinImageHandler(object):
    
    def __init__(self, conf, work_dir, image_dir, image_record_file, logger) -> None:
        self.conf = conf
        self.work_dir = work_dir
        self.image_dir = image_dir
        self.image_record_file = image_record_file
        self.LOG = logger

    def download_and_transform(self, images, img_to_download):

        # Download the image
        img_name = wget.filename_from_url(images['remote'][img_to_download]['path'])
        img_dict = copy.deepcopy(images['remote'][img_to_download])

        if not os.path.exists(os.path.join(self.image_dir, img_name)):
            self.LOG.debug(f'Downloading image: {img_to_download} from remote repo ...')
            img_dict['location'] = constants.IMAGE_LOCATION_LOCAL
            img_dict['status'] = constants.IMAGE_STATUS_DOWNLOADING
            images['local'][img_to_download] = img_dict
            omni_utils.save_image_data(self.image_record_file, images)
            wget.download(url=images['remote'][img_to_download]['path'], out=os.path.join(self.image_dir, img_name), bar=None)
            self.LOG.debug(f'Image: {img_to_download} succesfully downloaded from remote repo ...')
    
        # Decompress the image
        self.LOG.debug(f'Decompressing image file: {img_name} ...')
        qcow2_name = img_name[:-3]
        with open(os.path.join(self.image_dir, img_name), 'rb') as pr, open(os.path.join(self.image_dir, qcow2_name), 'wb') as pw:
            data = pr.read()
            data_dec = lzma.decompress(data)
            pw.write(data_dec)
    
        # Convert the qcow2 img to vhdx
        vhdx_name = img_to_download + '.vhdx'
        self.LOG.debug(f'Converting image file: {img_name} to {vhdx_name} ...')
        with powershell.PowerShell('GBK') as ps:
            cmd = 'qemu-img convert -O vhdx {0} {1}'
            outs, errs = ps.run(cmd.format(os.path.join(self.image_dir, qcow2_name), os.path.join(self.image_dir, vhdx_name)))
    
        # Record local image
        img_dict['status'] = constants.IMAGE_STATUS_READY
        img_dict['path'] = os.path.join(self.image_dir, vhdx_name)
        images['local'][img_to_download] = img_dict
        omni_utils.save_image_data(self.image_record_file, images)
        self.LOG.debug(f'Image: {img_to_download} is ready ...')

        # # TODO: Cleanup temp images?
        # pass