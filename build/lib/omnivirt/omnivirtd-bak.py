import json
import os
import wget
import lzma
import shutil
import time

from omnivirt import vmops
from omnivirt import utils
from omnivirt import constants
from omnivirt import powershell


CONFIG_FILE = 'D:\\omnivirt\\etc\\conf.yaml'

config_options = utils.check_and_load_config(CONFIG_FILE)

work_dir = config_options['work_dir']
image_dir = work_dir + constants.IMG_DIR
img_record_file = os.path.join(image_dir, 'images.json')
instance_dir = os.path.join(work_dir, 'instances')

_vmops = vmops.VMOps()


def init():
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    if not os.path.exists(img_record_file):
        image_body = {
            'images': []
        }
        with open(img_record_file, 'w', encoding='utf-8') as fw:
            json.dump(image_body, fw, indent=4, ensure_ascii=False)


def list_instances():
    vms = _vmops.list_instances()
    return vms

def list_images():
    with open(img_record_file, 'r', encoding='utf-8') as fr:
        local_images = json.load(fr)['images']
    
    local_img_names = []
    for img in local_images:
        local_img_names.append(img['image_id'])
    
    remote_images = list(constants.OPENEULER_IMGS.keys())
    ret = {
        'local': local_img_names,
        'remote': remote_images
    }

    return ret

def download_image(image_id):
    try:
        image_url = constants.OPENEULER_IMGS[image_id]
    except KeyError:
        raise

    # Download the image
    img_name = wget.filename_from_url(image_url)
    if not os.path.exists(os.path.join(image_dir, img_name)):
        print('Downloading image from remote repo, this might take a while ...\n')
        wget.download(url=image_url, out=os.path.join(image_dir, img_name))
    
    # Decompress the image
    print('Decompressing image ...\n')
    qcow2_name = img_name[:-3]
    with open(os.path.join(image_dir, img_name), 'rb') as pr, open(os.path.join(image_dir, qcow2_name), 'wb') as pw:
        data = pr.read()
        data_dec = lzma.decompress(data)
        pw.write(data_dec)
    
    # Convert the qcow2 img to vhdx
    vhdx_name = image_id + '.vhdx'
    print('Converting image ...\n')
    with powershell.PowerShell('GBK') as ps:
        cmd = 'qemu-img convert -O vhdx {0} {1}'
        outs, errs = ps.run(cmd.format(os.path.join(image_dir, qcow2_name), os.path.join(image_dir, vhdx_name)))
    
    # Record local image
    with open(img_record_file, 'r', encoding='utf-8') as fr:
        local_images = json.load(fr)['images']
    
    image_info = {
        'image_id': image_id,
        'image_path': os.path.join(image_dir, vhdx_name)
    }

    found = False
    for img in local_images:
        if img['image_id'] == image_id:
            img['image_path'] = image_info['image_path']
            found = True
            break
    
    if not found:
        local_images.append(image_info)
    
    image_body = {
            'images': local_images
        }
    with open(img_record_file, 'w', encoding='utf-8') as fw:
        json.dump(image_body, fw, indent=4, ensure_ascii=False)

    # TODO: Cleanup temp images?
    pass

def create_instance(vm_name, image_id):
    # Create dir for the instance
    vm_dict = {
        'Name': vm_name,
        'Image': image_id,
        'IP Address': ''
    }

    instance_path = os.path.join(instance_dir, vm_name)
    os.makedirs(instance_path)
    with open(img_record_file, 'r', encoding='utf-8') as fr:
        local_images = json.load(fr)['images']
    
    found = False
    founded_img = None
    for img in local_images:
        if img['image_id'] == image_id:
            founded_img = img['image_path']
            found = True
    
    if not found:
        print('Required image not availible locally, please download first')
        return False
    
    root_disk_path = shutil.copyfile(founded_img, os.path.join(instance_path, image_id + '.vhdx'))

    _vmops.build_and_run_vm(vm_name, image_id, False, 2, instance_path, root_disk_path)

    ip = _vmops.get_instance_ip_addr(vm_name)        

    vm_dict['ip'] = ip
    return vm_dict


#vm_name = 'test_omnivirt'
#instance_path = 'D:/vms/' + vm_name + '/'
#root_disk_path = 'D:\\vms\\openEuler-22.03-LTS-x86_64.vhdx'
# ret = my_vmops.build_and_run_vm(vm_name, False, 2, instance_path, root_disk_path)

#vms = my_vmops.list_instances()
#print(vms)

#info = my_vmops.get_info('test_python_2')

#print(info)

#note = my_vmops.get_instance_notes(vm_name)

#note = json.loads(note[0])

#vm_list = my_vmops.list_instances()

#for vm in vm_list:
#    print(vm.name)
#    print(vm.uuid)

# disk_info = my_vmops.get_vm_disks('test_omnivirt')

#my_vmops.attach_disk('test_python_3',  'D:\\vms\\openEuler-22.03-LTS-x86_64.vhdx', constants.DISK)

# my_vmops.power_up('test_python_3')

#my_vmops.add_nic('test_omnivirt', 'test_omnivirt_eth0')

#my_vmops.connect_vnic_to_switch('Default Switch', 'test_omnivirt_eth0')

#ports = my_vmops.list_switch_ports('Default Switch')
#print(ports)

#port = my_vmops.get_switch_port('Default Switch', 'test_omnivirt_eth0')
#print(port)

#nic = my_vmops.get_vm_nics('test_omnivirt', 'test_omnivirt_eth0')
#print(nics)

#ips = my_vmops.get_host_ips()
#print(ips)

#mac_address = utils.format_mac_addr(nic.Address)

#with powershell.PowerShell('GBK') as ps:
#    outs, errs = ps.run('arp -a | findstr /i {}'.format(mac_address))

#ip_address = outs.strip(' ').split(' ')[0]
#print(ip_address)

