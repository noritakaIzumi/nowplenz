import boto3
from botocore.exceptions import ClientError
import base64
import json


def __get_secret(secret_arn: str, region_name: str) -> dict:
    """トークンを取得する。

    例外が発生した場合は例外の内容を取得する。

    Notes:
        - トークンの内容は秘密なので Secrets Manager で管理します。
        - せっかく曲情報の格納で IAM ユーザのタグを使ってお金をケチったのに、ここでお金がかかります。

    Returns:

    """
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_arn
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            return {'exception': 'DecryptionFailureException'}
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            return {'exception': 'InternalServiceErrorException'}
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            return {'exception': 'InvalidParameterException'}
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            return {'exception': 'InvalidRequestException'}
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            return {'exception': 'ResourceNotFoundException'}
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return json.loads(secret)


def get_token(secret_arn: str, region_name: str) -> str:
    secret = __get_secret(secret_arn, region_name)
    return secret['token']
