import boto3
from collections import OrderedDict
from datetime import datetime
import uuid
from moto.core import BaseBackend, BaseModel

from tests.moto.greengrass.exceptions import InvalidContainerDefinitionException


class FakeGroup(BaseModel):
    def __init__(self, region_name, name):
        self.region_name = region_name
        self.group_id = str(uuid.uuid4())
        self.name = name
        self.arn = "arn:aws:greengrass:%s:1:/greengrass/groups/%s" % (self.region_name, self.group_id)
        self.created_at_datetime = datetime.utcnow()
        self.last_updated_datetime = datetime.utcnow()
        self.latest_version = ''
        self.latest_version_arn = ''

    def to_dict(self):
        res = {
            "Arn": self.arn,
            "CreationTimestamp": self.created_at_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "Id": self.group_id,
            "LastUpdatedTimestamp": self.last_updated_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "Name": self.name,
        }

        if self.latest_version:
            res["LatestVersion"] = self.latest_version
            res["LatestVersionArn"] = self.latest_version_arn

        return res


class FakeGroupVersion(BaseModel):
    def __init__(self, region_name, group_id, definition):
        self.region_name = region_name
        self.group_id = group_id
        self.version = str(uuid.uuid4())
        self.arn = "arn:aws:greengrass:%s:1:/greengrass/groups/%s/versions/%s" \
                   % (self.region_name, self.group_id, self.version)
        self.created_at_datetime = datetime.utcnow()
        self.definition = definition

    def to_dict(self):

        return {
            "Arn": self.arn,
            "CreationTimestamp": self.created_at_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "Definition": self.definition,
            "Id": self.group_id,
            "Version": self.version

        }


class GreengrassBackend(BaseBackend):
    def __init__(self, region_name):
        super(GreengrassBackend, self).__init__()
        self.region_name = region_name
        self.groups = OrderedDict()
        self.group_versions = OrderedDict()

    def reset(self):
        region_name = self.region_name
        self.__dict__ = {}
        self.__init__(region_name)

    def create_group(self, name, initial_version):

        if name == "":
            raise InvalidContainerDefinitionException(
                "Group name is missing in the input"
            )

        group = FakeGroup(self.region_name, name)
        self.groups[group.group_id] = group

        if initial_version:
            self.create_group_version(group.group_id, initial_version)

        return group

    def create_group_version(self, group_id, definition):
        # TODO Implement validation
        group_ver = FakeGroupVersion(self.region_name, group_id, definition)
        group_vers = self.group_versions.get(group_ver.group_id, {})
        group_vers[group_ver.version] = group_ver
        self.group_versions[group_ver.group_id] = group_vers
        self.groups[group_id].latest_version_arn = group_ver.arn
        self.groups[group_id].latest_version = group_ver.version
        return group_ver


available_regions = boto3.session.Session().get_available_regions("greengrass")
greengrass_backends = {region: GreengrassBackend(region) for region in available_regions}
