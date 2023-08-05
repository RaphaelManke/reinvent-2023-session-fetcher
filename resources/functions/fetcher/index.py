import json
import os
from typing import Any, Dict, Tuple
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from sessions_api import fetch_sessions
from models import ReInventSession
import boto3

logger = Logger()


def load_credentials() -> Tuple[str, str]:
    secretsmanager_client = boto3.client("secretsmanager")
    secret_value = secretsmanager_client.get_secret_value(
        SecretId=CREDENTIAL_SECRET_NAME
    )
    # extract the username and password fields from the secret string,
    # where the secret string is in the following JSON format:
    # {"username":"username","password":"password"}
    credentials_dict = json.loads(secret_value["SecretString"])
    username = credentials_dict["username"]
    password = credentials_dict["password"]
    return username, password


CREDENTIAL_SECRET_NAME = os.environ["CREDENTIAL_SECRET_NAME"]
USERNAME, PASSWORD = load_credentials()


def handler(_event: Dict[str, Any], _context: LambdaContext) -> None:
    raw_sessions = fetch_sessions(username=USERNAME, password=PASSWORD)

    for raw_session in raw_sessions[:5]:
        session = ReInventSession(**raw_session)
        print(session.model_dump_json(indent=2))


if __name__ == "__main__":
    handler({}, None)
