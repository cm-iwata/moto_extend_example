from __future__ import unicode_literals

import json

from moto.core.responses import BaseResponse
from tests.moto.greengrass.models import greengrass_backends


class GreengrassResponse(BaseResponse):
    SERVICE_NAME = "greengrass"

    @property
    def greengrass_backend(self):
        return greengrass_backends[self.region]

    def create_group(self):
        name = self._get_param("Name")
        initial_version = self._get_param("InitialVersion")
        res = self.greengrass_backend.create_group(name=name, initial_version=initial_version)
        return 201, {"status": 201}, json.dumps(res.to_dict())
