from omnivirt.grpcs.omnivirt_grpc import images_pb2


class Image(object):
    def __init__(self, client):
        self.client = client

    def list(self, filters):
        """Get list of images"""
        response = self.client.list_images()
        return response