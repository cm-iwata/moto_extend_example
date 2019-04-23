from __future__ import unicode_literals
from .models import greengrass_backends
from moto.core.models import base_decorator


greengrass_backend = greengrass_backends['us-east-1']
mock_greengrass = base_decorator(greengrass_backends)
