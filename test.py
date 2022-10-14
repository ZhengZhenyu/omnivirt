import os
import json
import wget
import lzma
import shutil
from omnivirt import constants
from omnivirt import powershell


ret = shutil.copyfile('D:\\omnivirt\\images\\22.03-LTS.vhdx', 'D:\\omnivirt\\instances\\22.03-LTS.vhdx')
print(ret)