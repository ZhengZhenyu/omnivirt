
# Copyright 2022 Zhenyu Zheng <zheng.zhenyu@outlook.com>
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""OmniVirt Base Exceptions.
"""
import logging

LOG = logging.getLogger(__name__)

class OmniVirtException(Exception):
    """Base OmniVirt Exception
    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.
    """
    msg_fmt = "An unknown exception occurred."
    code = 500
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        try:
            if not message:
                message = self.msg_fmt % kwargs
            else:
                message = str(message)
        except Exception:
            self._log_exception()
            message = self.msg_fmt

        self.message = message
        super(OmniVirtException, self).__init__(message)

    def _log_exception(self):
        LOG.exception('Exception in string format operation')
        for name, value in self.kwargs.items():
            LOG.error("%s: %s" % (name, value))  # noqa

    def format_message(self):
        return self.args[0]

    def __repr__(self):
        dict_repr = self.__dict__
        dict_repr['class'] = self.__class__.__name__
        return str(dict_repr)


class NoSuchFile(OmniVirtException):
    msg_fmt = "No Such File or Directory: %(file)s"

class NoConfigFileProvided(OmniVirtException):
    msg_fmt = "Config File Should Be Provided"