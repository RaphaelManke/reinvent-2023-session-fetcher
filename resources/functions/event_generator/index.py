import enum
import json
import datetime
from decimal import Decimal
import os
from typing import Any, Dict
import boto3
from boto3.dynamodb.types import TypeDeserializer
from deepdiff import DeepDiff


class EventType(enum.Enum):
    SessionAdded = "SessionAdded"
    SessionUpdated = "SessionUpdated"
    SessionRemoved = "SessionRemoved"


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)  # Convert Decimal to string representation
        return super(DecimalEncoder, self).default(o)


EVENT_BUS_NAME = os.environ["EVENT_BUS_NAME"]
EVENT_SOURCE = "ReInventSessionFetcher"
EVENT_VERSION = 1

EVENT_TYPE_MAP = {
    "INSERT": EventType.SessionAdded,
    "MODIFY": EventType.SessionUpdated,
    "REMOVE": EventType.SessionRemoved,
}

client = boto3.client("events")
deserializer = TypeDeserializer()


def handler(event: Dict[str, Any], _context: Any) -> None:
    for session_mutation_event in event["Records"]:
        match EVENT_TYPE_MAP.get(session_mutation_event["eventName"]):
            case EventType.SessionAdded:
                _handle_session_added(session_mutation_event)
            case EventType.SessionUpdated:
                _handle_session_update(session_mutation_event)
            case EventType.SessionRemoved:
                _handle_session_removed(session_mutation_event)


def _handle_session_added(event: dict):
    deserialized_session = {
        key: deserializer.deserialize(value)
        for key, value in event["dynamodb"]["NewImage"].items()
    }
    _send_event_to_event_bridge(EventType.SessionAdded, deserialized_session)


def _handle_session_update(event: dict):
    # Fetch the old session
    deserialized_old_session = {
        key: deserializer.deserialize(value)
        for key, value in event["dynamodb"]["OldImage"].items()
    }
    # Fetch the new session
    deserialized_new_session = {
        key: deserializer.deserialize(value)
        for key, value in event["dynamodb"]["NewImage"].items()
    }

    # Build a set of keys that are in both old and new sessions,
    # which should be compared for differences.
    keys_in_both_sessions_set = set(deserialized_old_session.keys()) & set(
        deserialized_new_session.keys()
    )
    for key in ["PK", "SK"]:
        keys_in_both_sessions_set.discard(key)

    # Build a dictionary of differences between the old and new sessions.
    diff_dict = {"added_keys": {}, "removed_keys": {}, "changed_keys": {}}

    # Loop over the new session and find keys that are not in the old session data.
    for key in [
        key
        for key in deserialized_new_session.keys()
        if key not in deserialized_old_session.keys()
    ]:
        diff_dict["added_keys"][key] = deserialized_new_session[key]

    # Loop over the old session and find keys that are not in the new session data.
    for key in [
        key
        for key in deserialized_old_session.keys()
        if key not in deserialized_new_session.keys()
    ]:
        diff_dict["removed_keys"][key] = deserialized_old_session[key]

    # Loop over the keys that are in both sessions and find differences.
    for key in list(keys_in_both_sessions_set):
        diff = DeepDiff(
            deserialized_old_session[key],
            deserialized_new_session[key],
            ignore_order=True,
        )
        if diff:
            diff_dict["changed_keys"][key] = diff

    # Send the event to the EventBridge Event Bus.
    _send_event_to_event_bridge(
        EventType.SessionUpdated,
        {
            "old": deserialized_old_session,
            "new": deserialized_new_session,
            "diff": diff_dict,
        },
    )


def _handle_session_removed(event: dict):
    deserialized_session = {
        key: deserializer.deserialize(value)
        for key, value in event["dynamodb"]["OldImage"].items()
    }
    _send_event_to_event_bridge(EventType.SessionRemoved, deserialized_session)


def _send_event_to_event_bridge(detail_type: EventType, event: dict):
    event_enveloped = {
        "metadata": {
            "eventVersion": EVENT_VERSION,
            "eventSource": EVENT_SOURCE,
            "eventType": detail_type.value,
            "eventDateTime": datetime.datetime.now(
                tz=datetime.timezone.utc
            ).isoformat(),
        },
        "data": event,
    }
    _put_events(
        source=EVENT_SOURCE,
        detail_type=detail_type.value,
        detail=json.dumps(event_enveloped, cls=DecimalEncoder),
        event_bus_name=EVENT_BUS_NAME,
    )


def _put_events(source: str, detail_type: str, detail: str, event_bus_name: str):
    client.put_events(
        Entries=[
            {
                "Source": source,
                "DetailType": detail_type,
                "Detail": detail,
                "EventBusName": event_bus_name,
            }
        ]
    )
