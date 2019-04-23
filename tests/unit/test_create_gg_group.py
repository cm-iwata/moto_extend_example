from botocore.exceptions import ClientError
import json
import pytest

from src.create_gg_group import handler


@pytest.mark.usefixtures('start_moto_mock')
class TestClass(object):

    def test_create_gg_group(self):

        event = {
            "body": {
                "grp_name": "test_grp"
            }
        }

        res = handler(event, {})
        data = json.loads(res)
        assert data["statusCode"] == 201
        assert data["body"]["Name"] == "test_grp"

    def test_empty_group_name(self):

        event = {
            "body": {
                "grp_name": ""
            }
        }

        with pytest.raises(ClientError) as ex:
            handler(event, {})
        assert ex.value.response["Error"]["Message"] == "Group name is missing in the input"
        assert ex.value.response["Error"]["Code"] == "InvalidContainerDefinitionException"
