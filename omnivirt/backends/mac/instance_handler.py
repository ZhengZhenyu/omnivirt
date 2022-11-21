import os
import shutil
import subprocess
import time

from oslo_utils import uuidutils

from omnivirt.utils import constants
from omnivirt.utils import utils as omni_utils
from omnivirt.utils import objs
from omnivirt.backends.mac import qemu


class MacInstanceHandler(object):
    
    def __init__(self, conf, work_dir, instance_dir, image_dir, image_record_file, logger) -> None:
        self.conf = conf
        self.work_dir = work_dir
        self.instance_dir = instance_dir
        self.instance_record_file = os.path.join(instance_dir, 'instances.json')
        self.image_dir = image_dir
        self.image_record_file = image_record_file
        self.driver = qemu.QemuDriver()
        self.running_instances = {}
        self.LOG = logger


    def list_instances(self):
        instances = omni_utils.load_json_data(self.instance_record_file)['instances']
        vm_list = []

        for instance in instances:
            vm = objs.Instance(name=instance['name'])
            vm.uuid = instance['uuid']
            vm.mac = instance['mac_address']
            vm.info = None
            vm.vm_state = None
            ip_address = self._parse_ip_addr(vm.mac)
            vm.ip = ip_address
            vm.image = None
            vm_list.append(vm)

        return vm_list

    def _parse_ip_addr(mac_addr):
        ip = ''
        cmd = f'arp -a | grep {mac_addr}'
        start_time = time.time()
        while(ip == '' and time.time() - start_time < 20):
            pr = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
            arp_result = pr.stdout
            arp_result = pr.stdout.decode('utf-8')
            try:
                ip = arp_result.split(' ')[1].replace("(", "").replace(")", "")
            except IndexError:
                continue
        
        return ip

    def create_instance(self, name, image_id, instance_record, all_instances, all_images):
        # Create dir for the instance
        vm_uuid = uuidutils.generate_uuid()
        vm_dict = {
            'name': name,
            'uuid': vm_uuid,
            'image': image_id,
            'vm_state': constants.VM_STATE_MAP[99],
            'ip_address': 'N/A',
            'mac_address': omni_utils.generate_mac(),
            'identification': {
                'type': 'pid',
                'id': None
            }
        }

        instance_path = os.path.join(self.instance_dir, name)
        os.makedirs(instance_path)
        img_path = all_images['local'][image_id]['path']
    
        root_disk_path = shutil.copyfile(img_path, os.path.join(instance_path, image_id + '.qcow2'))
        vm_process = self.driver.create_vm(name, vm_uuid, vm_dict['mac_address'], root_disk_path)
        self.running_instances[vm_process.pid] = vm_process
        vm_dict['identification']['id'] = vm_process.pid

        vm_ip = self._parse_ip_addr(vm_dict['mac_address'])
        vm_dict['ip_address'] = vm_ip

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
        # Delete instance process
        _vmops.delete_instance(name)

        # Cleanup files and records
        instance_dir = all_instances['instances'][name]['path']
        shutil.rmtree(instance_dir)
        del all_instances['instances'][name]

        omni_utils.save_json_data(instance_record, all_instances)

        return 0

