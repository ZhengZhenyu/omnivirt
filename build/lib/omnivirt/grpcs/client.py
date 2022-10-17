from urllib import request
import grpc

from omnivirt.grpcs.omnivirt_grpc import images_pb2, images_pb2_grpc
from omnivirt.grpcs import images
from omnivirt.utils import utils


class Client(object):
    def __init__(self, channel_target=None):
        if not channel_target:
            channel_target = 'localhost:50052'
        channel = grpc.insecure_channel(channel_target)

        images_client = images_pb2_grpc.GrpcServiceStub(channel)

        self._images = images.Image(images_client)


    @utils.response2dict
    def list_images(self, filters=None):
        """ [IMAGE] List images

        :param filters(list): None
        :return: dict -- list of images' info
        """

        return self._images.list()
    
    @utils.response2dict
    def download_image(self, name):
        """ Download image
        """

        return self._images.dowload(name)
