

from omnivirt.backends.win import powershell
from omnivirt.backends.win import vmops
from omnivirt.utils import constants
from omnivirt.utils import utils as omni_utils
from omnivirt.utils import objs


_vmops = vmops.VMOps()

class WinInstanceHandler(object):
    
    def __init__(self, conf, work_dir, image_dir, image_record_file, logger) -> None:
        self.conf = conf
        self.work_dir = work_dir
        self.image_dir = image_dir
        self.image_record_file = image_record_file
        self.LOG = logger

    def list_instances():
        vms = _vmops.list_instances()
        return vms