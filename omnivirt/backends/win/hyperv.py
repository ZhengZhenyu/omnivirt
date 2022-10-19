import os
import shutil

from omnivirt.backends.win import powershell
from omnivirt.backends.win import vmops
from omnivirt.utils import constants
from omnivirt.utils import utils as omni_utils
from omnivirt.utils import objs


_vmops = vmops.VMOps()

class WinInstanceHandler(object):
    
    def __init__(self, conf, work_dir, instance_dir, image_dir, image_record_file, logger) -> None:
        self.conf = conf
        self.work_dir = work_dir
        self.instance_dir = instance_dir
        self.image_dir = image_dir
        self.image_record_file = image_record_file
        self.LOG = logger

    def list_instances(self):
        vms = _vmops.list_instances()
        return vms
    
    def create_instance(self, name, image_id, all_images):
            # Create dir for the instance
        vm_dict = {
            'name': name,
            'image': image_id,
            'vm_state': constants.VM_STATE_MAP[99],
            'ip_address': 'N/A'
        }

        instance_path = os.path.join(self.instance_dir, name)
        os.makedirs(instance_path)
        img_path = all_images['local'][image_id]['path']
    
        root_disk_path = shutil.copyfile(img_path, os.path.join(instance_path, image_id + '.vhdx'))
        _vmops.build_and_run_vm(name, image_id, False, 2, instance_path, root_disk_path)

        info = _vmops.get_info(name)
        vm_dict['vm_state'] = constants.VM_STATE_MAP[info['EnabledState']]
        ip = _vmops.get_instance_ip_addr(name)
        if ip: 
            vm_dict['ip_address'] = ip

        return vm_dict