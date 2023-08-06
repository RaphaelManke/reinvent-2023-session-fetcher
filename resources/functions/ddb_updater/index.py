from typing import Dict, Any
import enum
import os
import json
import boto3
from aws_lambda_powertools.utilities.typing import LambdaContext


class EventType(enum.Enum):
    SessionAdded = "SessionAdded"
    SessionUpdated = "SessionUpdated"
    SessionRemoved = "SessionRemoved"


DDB_TABLE_NAME = os.environ["DDB_TABLE_NAME"]
DDB_RESOURCE = boto3.resource("dynamodb")

TABLE = DDB_RESOURCE.Table(DDB_TABLE_NAME)


def handler(event: Dict[str, Any], _context: LambdaContext) -> None:
    detail_type = event["detail-type"]
    if detail_type not in EventType.__members__:
        raise Exception(f"Unknown detail type: {detail_type}")

    _write_mutation_to_ddb(
        event_type=EventType(detail_type),
        source_event=event["detail"],
    )


def _write_mutation_to_ddb(event_type: EventType, source_event: dict):
    print(event_type.value)
    session_id = None
    match event_type.value:
        case "SessionRemoved":
            session_id = source_event["data"]["thirdPartyID"]
        case "SessionAdded":
            session_id = source_event["data"]["thirdPartyID"]
        case "SessionUpdated":
            session_id = source_event["data"]["new"]["thirdPartyID"]

    item_data = {
        "PK": "SessionMutation",
        "SK": source_event["metadata"]["eventDateTime"],
    } | {
        "mutationType": event_type.value,
        "sessionID": session_id,
        "mutationData": source_event["data"],
    }

    TABLE.put_item(Item=item_data)
