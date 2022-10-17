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
        img_name = wget.filename_from_url(images[img_to_download]['path'])
        if not os.path.exists(os.path.join(self.image_dir, img_name)):
            self.LOG.debug(f'Downloading image: {img_to_download} from remote repo ...')
            images[img_to_download]['status'] = constants.IMAGE_STATUS_DOWNLOADING
            omni_utils.save_image_data(self.image_record_file, images)
            wget.download(url=images[img_to_download]['path'], out=os.path.join(self.image_dir, img_name), bar=None)
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
        images[img_to_download]['path'] = os.path.join(self.image_dir, vhdx_name)
        omni_utils.save_image_data(self.image_record_file, images)
        with powershell.PowerShell('GBK') as ps:
            cmd = 'qemu-img convert -O vhdx {0} {1}'
            outs, errs = ps.run(cmd.format(os.path.join(self.image_dir, qcow2_name), os.path.join(self.image_dir, vhdx_name)))
    
        # Record local image
        images[img_to_download]['status'] = constants.IMAGE_STATUS_READY
        images[img_to_download]['path'] = os.path.join(self.image_dir, vhdx_name)
        omni_utils.save_image_data(self.image_record_file, images)
        self.LOG.debug(f'Image: {img_to_download} is ready ...')

        # # TODO: Cleanup temp images?
        # pass