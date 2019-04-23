import boto3
import json


gg_client = boto3.client("greengrass", region_name="ap-northeast-1")


def handler(event, context):

    grp_name = event['body']['grp_name']
    res = gg_client.create_group(Name=grp_name)

    return json.dumps({
        "statusCode": 201,
        "body": res
    })
