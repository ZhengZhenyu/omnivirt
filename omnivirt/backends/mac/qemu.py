import subprocess


class QemuDriver(object):

    def __init__(self) -> None:
        self.qemu_bin = '/opt/homebrew/bin/qemu-system-aarch64'
        self.uefi_file = '/opt/homebrew/Cellar/qemu/7.1.0/share/qemu/edk2-aarch64-code.fd'
        self.uefi_params = ',if=pflash,format=raw,readonly=on'
    
    def create_vm(self, vm_name, vm_uuid, vm_mac, vm_root_disk):
        qemu_cmd = [self.qemu_bin, '-name', vm_name, '-uuid',
            vm_uuid, '-machine', 'virt,highmem=off', '-accel hvf', '-drive',
            'file=' + self.uefi_file + self.uefi_params, '-cpu host',
            '-nic', 'vmnet-shared,model=virtio-net-pci,mac=' + vm_mac,
            '-drive', 'file=' + vm_root_disk, '-device', 'virtio-scsi-pci,id=scsi0',
            '-smp', '1', '-m', '1024M', '-monitor none -chardev null,id=char0',
            '-serial chardev:char0 -nographic']

        instance_process = subprocess.Popen(' '.join(qemu_cmd), shell=True)
        return instance_process
