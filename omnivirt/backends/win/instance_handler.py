import os
import shutil

from oslo_utils import uuidutils

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
        self.instance_record_file = os.path.join(instance_dir, 'instances.json')
        self.image_dir = image_dir
        self.image_record_file = image_record_file
        self.LOG = logger

    def list_instances(self):
        vms = _vmops.list_instances()
        return vms
    
    def create_instance(self, name, image_id, instance_record, all_instances, all_images):
        # Create dir for the instance
        vm_dict = {
            'name': name,
            'uuid': uuidutils.generate_uuid(),
            'image': image_id,
            'vm_state': constants.VM_STATE_MAP[99],
            'ip_address': 'N/A',
            'mac_address': 'N/A',
            'identification': {
                'type': 'name',
                'id': name
            }
        }

        instance_path = os.path.join(self.instance_dir, name)
        os.makedirs(instance_path)
        img_path = all_images['local'][image_id]['path']
    
        root_disk_path = shutil.copyfile(img_path, os.path.join(instance_path, image_id + '.vhdx'))
        _vmops.build_and_run_vm(name, vm_dict['uuid'], image_id, False, 2, instance_path, root_disk_path)

        info = _vmops.get_info(name)
        vm_dict['vm_state'] = constants.VM_STATE_MAP[info['EnabledState']]
        ip = _vmops.get_instance_ip_addr(name)
        if ip: 
            vm_dict['ip_address'] = ip
        
        instance_record_dict = {
            'name': name,
            'uuid': vm_dict['uuid'],
            'image': image_id,
            'path': instance_path,
            'mac_address': vm_dict['mac_address'],
            'ip_address': vm_dict['ip_address'],
            'identification': vm_dict['identification']
        }

        all_instances['instances'][name] = instance_record_dict
        omni_utils.save_json_data(instance_record, all_instances)

        return vm_dict
    
    def delete_instance(self, name, instance_record, all_instances):
        # Delete instance
        _vmops.delete_instance(name)

        # Cleanup files and records
        instance_dir = all_instances['instances'][name]['path']
        shutil.rmtree(instance_dir)
        del all_instances['instances'][name]

        omni_utils.save_json_data(instance_record, all_instances)

        return 0
