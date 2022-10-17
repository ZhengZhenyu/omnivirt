import grpc
import os

from omnivirt.grpcs.omnivirt_grpc import images_pb2, images_pb2_grpc
from omnivirt.grpcs import images
from omnivirt.utils import constants
from omnivirt.utils import utils as omnivirt_utils


class Client(object):
    def __init__(self, channel_target=None):
        if not channel_target:
            channel_target = 'localhost:50052'
        channel = grpc.insecure_channel(channel_target)

        images_client = images_pb2_grpc.GrpcServiceStub(channel)

        self._images = images.Image(images_client)


    @omnivirt_utils.response2dict
    def list_images(self, filters=None):
        """ [IMAGE] List images

        :param filters(list): None
        :return: dict -- list of images' info
        """

        return self._images.list()
    
    @omnivirt_utils.response2dict
    def download_image(self, name):
        """ Download image
        """

        return self._images.download(name)

    @omnivirt_utils.response2dict
    def load_image(self, name, path):
        """ Load local image file
        """
        
        if not os.path.exists(path):
            err_msg = {
                'ret': 1,
                'msg': f'No such file or directory: {path}, please check again.'
            }
            return err_msg
        
        supported = False
        for tp in constants.IMAGE_LOAD_SUPPORTED_TYPES:
            if path.endswith(tp):
                supported = True
                break
        
        if not supported:
            err_msg = {
                'ret': 1,
                'msg': f'Image file format does not supported: {path}, please check again.'
            }
            return err_msg
        
        return self._images.load(name, path)

    @omnivirt_utils.response2dict
    def delete_image(self, name):
        """ Delete the requested image
        """

        return self._images.delete(name)
