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
        # TODO: Use different backend for different OS
        self.backend = win_image_handler.WinImageHandler(
            self.CONF, self.work_dir, self.image_dir, self.img_record_file, LOG)

    def list_images(self, request, context):
        LOG.debug(f"Get request to list images ...")
        all_images = utils.load_image_data(self.img_record_file)

        ret = []
        for _, images in all_images.items():
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
        all_images = utils.load_image_data(self.img_record_file)
        
        if request.name not in all_images['remote'].keys():
            LOG.debug(f'Image: {request.name} not valid for download')
            msg = f'Error: Image {request.name} is valid for download, please check image name from REMOTE IMAGE LIST using "images" command ...'
            return images_pb2.GeneralImageResponse(ret=1, msg=msg)
        
        @utils.asyncwrapper
        def do_download(images, name):
            self.backend.download_and_transform(images, name)
        
        do_download(all_images, request.name)

        msg = f'Downloading: {request.name}, this might take a while, please check image status with "images" command.'
        return images_pb2.GeneralImageResponse(ret=0, msg=msg)

    def load_image(self, request, context):
        LOG.debug(f"Get request to load image: {request.name} from path: {request.path} ...")
        all_images = utils.load_image_data(self.img_record_file)

        msg = f'Loading: {request.name}, this might take a while, please check image status with "images" command.'
        update = False

        local_images = all_images['local']
        if request.name in local_images.keys():
            LOG.debug(f"Image: {request.name} already existed, replace it with: {request.path} ...")
            msg = f'Replacing: {request.name}, with new image file: {request.path}, this might take a while, please check image status with "images" command.'
            update = True

        @utils.asyncwrapper
        def do_load(images, name, path, update):
            self.backend.load_and_transform(images, name, path, update)
        
        do_load(all_images, request.name, request.path, update)

        return images_pb2.GeneralImageResponse(ret=0, msg=msg)

    def delete_image(self, request, context):
        LOG.debug(f"Get request to delete image: {request.name}  ...")
        images = utils.load_image_data(self.img_record_file)
        ret = self.backend.delete_image(images, request.name)
        if ret == 0:
            msg = f'Image: {request.name} has been successfully deleted.'
        elif ret == 1:
            msg = f'Image: {request.name} does not exist, please check again.'

        return images_pb2.GeneralImageResponse(ret=0, msg=msg)
