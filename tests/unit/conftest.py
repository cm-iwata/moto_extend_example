import moto
import pytest

from tests.moto.greengrass import mock_greengrass


@pytest.fixture()
def start_moto_mock():
    moto.mock_iot().start()
    moto.mock_sts().start()
    moto.mock_iotdata().start()
    moto.mock_dynamodb2().start()
    moto.mock_s3().start()
    mock_greengrass().start()
    moto.mock_lambda().start()

    yield

    moto.mock_iot().stop()
    moto.mock_sts().stop()
    moto.mock_iotdata().stop()
    moto.mock_dynamodb2().stop()
    moto.mock_s3().stop()
    mock_greengrass().stop()
    moto.mock_lambda().stop()
