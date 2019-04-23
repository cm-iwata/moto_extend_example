from __future__ import unicode_literals
from moto.core.exceptions import JsonRESTError


class GreengrassClientError(JsonRESTError):
    code = 400


class InvalidContainerDefinitionException(GreengrassClientError):
    def __init__(self, msg):
        self.code = 400
        super(InvalidContainerDefinitionException, self).__init__(
            "InvalidContainerDefinitionException",
            msg
        )
