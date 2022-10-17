import json
import logging
import os

from omnivirt.backends.win import image_handler as win_image_handler
from omnivirt.grpcs.omnivirt_grpc import images_pb2, images_pb2_grpc
from omnivirt.utils import utils


LOG = logging.getLogger(__name__)


class ImagerService(images_pb2_grpc.GrpcServiceServicer):
    '''
    The Imager GRPC Handler
    '''

    def __init__(self, conf) -> None:
        self.CONF = conf
        self.work_dir = self.CONF.conf.get('default', 'work_dir')
        self.image_dir = os.path.join(self.work_dir, self.CONF.conf.get('default', 'image_dir'))
        self.img_record_file = os.path.join(self.image_dir, 'images.json')
        self.backend = win_image_handler.WinImageHandler(
            self.CONF, self.work_dir, self.image_dir, self.img_record_file, LOG)

    def load_data(self):
        return utils.load_image_data(self.img_record_file)
    
    def save_data(self, data):
        return utils.save_image_data(self.img_record_file, data)

    def list_images(self, request, context):
        LOG.debug(f"Get request to list images ...")
        images = self.load_data()

        ret = []
        for _, img in images.items():
            image = images_pb2.Image()
            image.name = img['name']
            image.location = img['location']
            image.status = img['status']
            ret.append(image)
        LOG.debug(f"Responded: {ret}")
        return images_pb2.ListImageResponse(images=ret)
    
    def download_image(self, request, context):
        LOG.debug(f"Get request to download image: {request.name} ...")
        images = self.load_data()
        
        if request.name not in images.keys():
            LOG.debug(f'Image: {request.name} not valid for download')
            msg = f'Error: Image {request.name} is valid for download, please check image name from REMOTE IMAGE LIST using "images" command ...'
            return images_pb2.DownloadImageResponse(ret=1, msg=msg)
        
        @utils.asyncwrapper
        def do_download(images, name):
            self.backend.download_and_transform(images, name)
        
        do_download(images, request.name)

        msg = f'Downloading: {request.name} this might take a while, please check image status with "images" command.'
        return images_pb2.DownloadImageResponse(ret=0, msg=msg)
