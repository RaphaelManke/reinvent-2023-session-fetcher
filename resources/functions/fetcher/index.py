from typing import Any, Dict
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from sessions_api import fetch_sessions
from models import ReInventSession


logger = Logger()


def handler(_event: Dict[str, Any], _context: LambdaContext) -> None:
    raw_sessions = fetch_sessions()

    for raw_session in raw_sessions[:5]:
        session = ReInventSession(**raw_session)
        print(session.model_dump_json(indent=2))


if __name__ == "__main__":
    handler({}, None)
