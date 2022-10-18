from omnivirt.grpcs.omnivirt_grpc import instances_pb2

class Instance(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        """Get list of instance"""
        request = instances_pb2.ListInstancesRequest()
        response = self.client.list_instances(request)
        return response
