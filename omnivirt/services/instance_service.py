import logging
import os

from omnivirt.backends.win import hyperv as win_instance_handler
from omnivirt.grpcs.omnivirt_grpc import instances_pb2, instances_pb2_grpc
from omnivirt.utils import utils


LOG = logging.getLogger(__name__)

class InstanceService(instances_pb2_grpc.GrpcServiceServicer):
    '''
    The Instance GRPC Handler
    '''

    def __init__(self, conf) -> None:
        self.CONF = conf
        self.work_dir = self.CONF.conf.get('default', 'work_dir')
        self.image_dir = os.path.join(self.work_dir, self.CONF.conf.get('default', 'image_dir'))
        self.img_record_file = os.path.join(self.image_dir, 'images.json')
        # TODO: Use different backend for different OS
        self.backend = win_instance_handler.WinInstanceHandler(
            self.CONF, self.work_dir, self.image_dir, self.img_record_file, LOG)

    def list_instances(self, request, context):
        LOG.debug(f"Get request to list instances ...")
        instances_obj = self.backend.list_instances()

        ret = []
        for vm_obj in instances_obj:
            instance_dict = {
                'name': vm_obj.name,
                'image': vm_obj.image,
                'ip': vm_obj.ip
            }
            ret.append(instance_dict)
            
        return instances_pb2.ListInstancesResponse(instances=ret)