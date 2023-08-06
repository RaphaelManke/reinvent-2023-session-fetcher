import json
import os
import pprint
from typing import Any, Dict

import requests
from _example_payload import example_payload
from models import ReInventSession
from aws_lambda_powertools.utilities import parameters

from slack_message import map_session_to_slack_block


slack_webhook_url: str = parameters.get_secret(
    os.getenv("SLACK_WEBHOOK_URL_SECRET_NAME")
)


def handler(event: Dict[str, Any], _context: Any):
    body = event["Records"][0]["body"]
    body_json = json.loads(body)
    event_detail = body_json["detail"]
    event_detail_type = body_json["detail-type"]
    if event_detail_type == "SessionUpdated":
        new_session = event_detail["new"]
        session = ReInventSession(**new_session)
        slack_message = map_session_to_slack_block(
            session=session, change_type=event_detail_type
        )
        slack_message["blocks"].append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*diff*\n```{json.dumps(event_detail['diff'], indent=2)}```",
                },
            }
        )
    else:
        session = ReInventSession(**event_detail)
        slack_message = map_session_to_slack_block(
            session=session, change_type=event_detail_type
        )
    requests.post(slack_webhook_url, json=slack_message)

    return slack_message


if __name__ == "__main__":
    handler(example_payload, None)
