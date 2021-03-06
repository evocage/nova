# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Canonical Ltd
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

"""Render Vendordata as stored in configured file."""

import errno

from oslo.config import cfg

from nova.api.metadata import base
from nova.openstack.common.gettextutils import _
from nova.openstack.common import jsonutils
from nova.openstack.common import log as logging

file_opt = cfg.StrOpt('vendordata_jsonfile_path',
                      default=None,
                      help='File to load json formated vendor data from')

CONF = cfg.CONF
CONF.register_opt(file_opt)
LOG = logging.getLogger(__name__)


class JsonFileVendorData(base.VendorDataDriver):
    def __init__(self, *args, **kwargs):
        super(JsonFileVendorData, self).__init__(*args, **kwargs)
        data = {}
        fpath = CONF.vendordata_jsonfile_path
        logprefix = "%s[%s]: " % (file_opt.name, fpath)
        if fpath:
            try:
                with open(fpath, "r") as fp:
                    data = jsonutils.load(fp)
            except IOError as e:
                if e.errno == errno.ENOENT:
                    LOG.warn(logprefix + _("file does not exist"))
                else:
                    LOG.warn(logprefix + _("Unexpected IOError when reading"))
                raise e
            except ValueError:
                LOG.warn(logprefix + _("failed to load json"))
                raise

        self._data = data

    def get(self):
        return self._data
