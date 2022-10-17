from omnivirt.grpcs.omnivirt_grpc import images_pb2


class Image(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        """Get list of images"""
        request = images_pb2.ListImageRequest()
        response = self.client.list_images(request)
        return response
    
    def dowload(self, name):
        """Download the requested image"""
        request = images_pb2.DownloadImageRequest(name=name)
        response = self.client.download_image(request)
        return response