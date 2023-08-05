import json
import os
from typing import Any, Dict, Tuple, List
from aws_lambda_powertools.utilities.typing import LambdaContext

from sessions_api import fetch_sessions
from controllers.session_controller import SessionController
from models import ReInventSession
import boto3

CREDENTIAL_SECRET_NAME = os.environ["CREDENTIAL_SECRET_NAME"]
DB_TABLE_NAME = os.environ["DB_TABLE_NAME"]


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


USERNAME, PASSWORD = load_credentials()


def handler(_event: Dict[str, Any], _context: LambdaContext) -> None:
    raw_sessions = fetch_sessions(username=USERNAME, password=PASSWORD)

    session_models_from_api: List[ReInventSession] = [
        ReInventSession(**raw_session) for raw_session in raw_sessions[2:3]
    ]

    if not session_models_from_api:
        raise RuntimeError("No sessions found, bailing.")

    session_controller = SessionController(db_table_name=DB_TABLE_NAME)
    diff = session_controller.generate_diff(new_session_list=session_models_from_api)
    session_controller.insert_new_sessions(
        new_session_list=diff.added_sessions.values()
    )
    session_controller.remove_sessions(session_list=diff.removed_sessions.values())
    session_controller.update_sessions(
        updated_session_list=[
            session_diff.new_session for session_diff in diff.updated_sessions.values()
        ]
    )


if __name__ == "__main__":
    handler({}, None)
