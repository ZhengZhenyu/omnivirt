class Instance(object):

    def __init__(self, name='') -> None:
        self.name = name
        self.uuid = ''
        self.metadata = None
        self.vm_state = None
        self.vcpu = None
        self.ram = None
        self.disk = None
        self.vm_state = None
        self.info = None
        self.image = None
        self.ip = None
