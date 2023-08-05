import enum
import json
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
    deserialized_old_session = {
        key: deserializer.deserialize(value)
        for key, value in event["dynamodb"]["OldImage"].items()
    }
    deserialized_new_session = {
        key: deserializer.deserialize(value)
        for key, value in event["dynamodb"]["NewImage"].items()
    }

    diff = DeepDiff(
        deserialized_old_session,
        deserialized_new_session,
        ignore_order=True,
    )

    _send_event_to_event_bridge(
        EventType.SessionUpdated,
        {
            "old": deserialized_old_session,
            "new": deserialized_new_session,
            "diff": diff.to_dict(),
        },
    )


def _handle_session_removed(event: dict):
    deserialized_session = {
        key: deserializer.deserialize(value)
        for key, value in event["dynamodb"]["OldImage"].items()
    }
    _send_event_to_event_bridge(EventType.SessionRemoved, deserialized_session)


def _send_event_to_event_bridge(detail_type: EventType, event: dict):
    client.put_events(
        Entries=[
            {
                "Source": EVENT_SOURCE,
                "DetailType": detail_type.value,
                "Detail": json.dumps(event, cls=DecimalEncoder),
                "EventBusName": EVENT_BUS_NAME,
            }
        ]
    )


if __name__ == "__main__":
    event = {
        "Records": [
            {
                "eventID": "9c4a47184276fd0627543d4285bb4bc5",
                "eventName": "INSERT",
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "eu-west-1",
                "dynamodb": {
                    "ApproximateCreationDateTime": 1691273511.0,
                    "Keys": {"SK": {"S": "SVS309"}, "PK": {"S": "ReInventSession"}},
                    "NewImage": {
                        "level": {"N": "300"},
                        "topics": {"L": [{"S": "Serverless Compute"}]},
                        "roles": {
                            "L": [
                                {"S": "DevOps Engineer"},
                                {"S": "Solution/Systems Architect"},
                                {"S": "Developer/Engineer"},
                            ]
                        },
                        "scheduleUid": {"S": "706791CC-1EB3-4E2C-9C66-008E2342CD9C"},
                        "description": {
                            "S": "Enterprise-based serverless developers are often subject to constraints and compliance checks that can slow deployment and feedback loops. Shift-left practices can empower developers with tools that help test and validate code compliance prior to committing to repositories. In this session, learn about approaches to accelerate serverless development with faster feedback cycles. Explore best practices and tools with Capital One. Watch a live demo featuring an improved developer experience for building serverless applications while complying with enterprise governance requirements."
                        },
                        "services": {
                            "L": [
                                {"S": "AWS Serverless Application Model (SAM)"},
                                {"S": "AWS Lambda"},
                            ]
                        },
                        "trackName": {"S": "Breakout Session"},
                        "title": {
                            "S": "Improve productivity by shifting more responsibility to developers"
                        },
                        "tags": {
                            "L": [
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "16A05B04-62C9-45E5-A5AC-79CB47268800"
                                        },
                                        "parentTagUid": {
                                            "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                        },
                                        "tagName": {"S": "DevOps Engineer"},
                                        "parentTagName": {"S": "Role"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "FEA56535-2467-4B81-A23B-3AD277FD5F4E"
                                        },
                                        "parentTagUid": {
                                            "S": "F2BB2A9C-8783-4072-A0A4-5621D1A481A6"
                                        },
                                        "tagName": {"S": "Serverless Compute"},
                                        "parentTagName": {"S": "Topic"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "3859EA66-BDDD-455E-A49F-341CD14EFBBA"
                                        },
                                        "parentTagUid": {
                                            "S": "7A26869A-A0C9-48CC-9731-541C3AFA9DF4"
                                        },
                                        "tagName": {
                                            "S": "AWS Serverless Application Model (SAM)"
                                        },
                                        "parentTagName": {"S": "Services"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "2CABCC3D-F2BB-490C-9265-8CBB7660C579"
                                        },
                                        "parentTagUid": {
                                            "S": "2634F5B6-B8E0-4208-92C3-FAE426C930F7"
                                        },
                                        "tagName": {"S": "300 - Advanced"},
                                        "parentTagName": {"S": "Level"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "C15716B3-CC11-433E-B619-8EE42AF15F6B"
                                        },
                                        "parentTagUid": {
                                            "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                        },
                                        "tagName": {"S": "Solution/Systems Architect"},
                                        "parentTagName": {"S": "Role"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "4F085EF2-7954-4A96-9A8C-45BC0EC61359"
                                        },
                                        "parentTagUid": {
                                            "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                        },
                                        "tagName": {"S": "Developer/Engineer"},
                                        "parentTagName": {"S": "Role"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "BDA0A04D-E32F-425E-917A-8FEFE5B563D3"
                                        },
                                        "parentTagUid": {
                                            "S": "7A26869A-A0C9-48CC-9731-541C3AFA9DF4"
                                        },
                                        "tagName": {"S": "AWS Lambda"},
                                        "parentTagName": {"S": "Services"},
                                    }
                                },
                            ]
                        },
                        "thirdPartyID": {"S": "SVS309"},
                        "industries": {"L": []},
                        "sessionUid": {"S": "BD8998F7-BD38-474F-A5F9-44CDF5502BF4"},
                        "SK": {"S": "SVS309"},
                        "sessionType": {"S": "Breakout Session"},
                        "scheduleTrackUid": {
                            "S": "CEDEEA9B-CDE9-ED11-81DB-A4AC1C44CA4E"
                        },
                        "PK": {"S": "ReInventSession"},
                        "areas_of_interest": {"L": []},
                    },
                    "SequenceNumber": "17525900000000051699273399",
                    "SizeBytes": 2198,
                    "StreamViewType": "NEW_AND_OLD_IMAGES",
                },
                "eventSourceARN": "arn:aws:dynamodb:eu-west-1:739178438747:table/ReInventSessionTable/stream/2023-08-05T21:30:53.861",
            },
            {
                "eventID": "675338e108b9547a0c2958fbda56a29a",
                "eventName": "REMOVE",
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "eu-west-1",
                "dynamodb": {
                    "ApproximateCreationDateTime": 1691273511.0,
                    "Keys": {"SK": {"S": "CMP403"}, "PK": {"S": "ReInventSession"}},
                    "OldImage": {
                        "level": {"N": "400"},
                        "topics": {"L": [{"S": "Compute"}]},
                        "roles": {
                            "L": [
                                {"S": "Data Engineer"},
                                {"S": "Developer/Engineer"},
                                {"S": "IT Administrator"},
                            ]
                        },
                        "scheduleUid": {"S": "A7956934-FF28-473D-96A8-012D497C6716"},
                        "description": {
                            "S": "Amazon EC2 Auto Scaling groups empower users to benefit from the elasticity benefits of the AWS Cloud. In this workshop, learn how you can make the most of the latest innovations from EC2 Auto Scaling to improve your web application availability at lower costs. Specifically, find out how to use a combination of predictive scaling, dynamic scaling, and warm pool features to automatically launch and terminate capacity with changing demands. With more responsive and proactive scaling, you run only the required number of instances at any time of the day, reducing the cost of overprovisioned EC2 instances. You must bring your laptop to participate."
                        },
                        "services": {
                            "L": [
                                {"S": "Amazon EC2 Auto Scaling"},
                                {"S": "Amazon Elastic Compute Cloud (EC2)"},
                            ]
                        },
                        "trackName": {"S": "updated track name"},
                        "title": {
                            "S": "Proactive auto scaling for optimal cost and availability"
                        },
                        "tags": {
                            "L": [
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "CCEE8B58-D74C-4469-8FE4-19F0C692CC6C"
                                        },
                                        "parentTagUid": {
                                            "S": "7A26869A-A0C9-48CC-9731-541C3AFA9DF4"
                                        },
                                        "tagName": {"S": "Amazon EC2 Auto Scaling"},
                                        "parentTagName": {"S": "Services"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "7807988D-1640-44DE-B5D4-CAB4A3D98CC1"
                                        },
                                        "parentTagUid": {
                                            "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                        },
                                        "tagName": {"S": "Data Engineer"},
                                        "parentTagName": {"S": "Role"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "4F085EF2-7954-4A96-9A8C-45BC0EC61359"
                                        },
                                        "parentTagUid": {
                                            "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                        },
                                        "tagName": {"S": "Developer/Engineer"},
                                        "parentTagName": {"S": "Role"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "DE0F6885-27E7-4BAC-AB2C-A234A7F6BCCB"
                                        },
                                        "parentTagUid": {
                                            "S": "F2BB2A9C-8783-4072-A0A4-5621D1A481A6"
                                        },
                                        "tagName": {"S": "Compute"},
                                        "parentTagName": {"S": "Topic"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "F42B9C9D-C9B8-4399-8F91-658AAA167ED9"
                                        },
                                        "parentTagUid": {
                                            "S": "B78A961D-DC03-42C9-A32E-DA576734A89E"
                                        },
                                        "tagName": {"S": "Cross Industry "},
                                        "parentTagName": {"S": "Industry"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "B2CA25EB-C2BD-42B2-9FC5-0B607ACD4C19"
                                        },
                                        "parentTagUid": {
                                            "S": "7A26869A-A0C9-48CC-9731-541C3AFA9DF4"
                                        },
                                        "tagName": {
                                            "S": "Amazon Elastic Compute Cloud (EC2)"
                                        },
                                        "parentTagName": {"S": "Services"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "B6C0FC98-BE24-4ABB-8B2C-939AF5F58363"
                                        },
                                        "parentTagUid": {
                                            "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                        },
                                        "tagName": {"S": "IT Administrator"},
                                        "parentTagName": {"S": "Role"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "20445AB2-C0C4-4DE2-9443-F1B9780A69CE"
                                        },
                                        "parentTagUid": {
                                            "S": "3428EB86-4D79-4EFE-9F33-E911FCC500A4"
                                        },
                                        "tagName": {"S": "Migration & Transfer"},
                                        "parentTagName": {"S": "Area of Interest"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "594D1AC5-4EDB-442A-BD5E-EE580E43441E"
                                        },
                                        "parentTagUid": {
                                            "S": "3428EB86-4D79-4EFE-9F33-E911FCC500A4"
                                        },
                                        "tagName": {"S": "Cost Optimization"},
                                        "parentTagName": {"S": "Area of Interest"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "6F2C43D3-196B-4957-82C5-9F46BAC3DE5E"
                                        },
                                        "parentTagUid": {
                                            "S": "2634F5B6-B8E0-4208-92C3-FAE426C930F7"
                                        },
                                        "tagName": {"S": "400 - Expert"},
                                        "parentTagName": {"S": "Level"},
                                    }
                                },
                            ]
                        },
                        "thirdPartyID": {"S": "CMP403"},
                        "industries": {"L": [{"S": "Cross Industry"}]},
                        "sessionUid": {"S": "E32C1CD6-D674-4966-B1EA-8E5D082F906F"},
                        "SK": {"S": "CMP403"},
                        "sessionType": {"S": "Workshop"},
                        "scheduleTrackUid": {
                            "S": "5F87F61B-CEE9-ED11-81DB-A4AC1C44CA4E"
                        },
                        "PK": {"S": "ReInventSession"},
                        "areas_of_interest": {
                            "L": [
                                {"S": "Migration & Transfer"},
                                {"S": "Cost Optimization"},
                            ]
                        },
                    },
                    "SequenceNumber": "17526000000000051699273518",
                    "SizeBytes": 2741,
                    "StreamViewType": "NEW_AND_OLD_IMAGES",
                },
                "eventSourceARN": "arn:aws:dynamodb:eu-west-1:739178438747:table/ReInventSessionTable/stream/2023-08-05T21:30:53.861",
            },
            {
                "eventID": "30cb134b2e849caaa65905dd9119f8aa",
                "eventName": "MODIFY",
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "eu-west-1",
                "dynamodb": {
                    "ApproximateCreationDateTime": 1691273102.0,
                    "Keys": {"SK": {"S": "CMP403"}, "PK": {"S": "ReInventSession"}},
                    "NewImage": {
                        "level": {"N": "400"},
                        "topics": {"L": [{"S": "Compute"}]},
                        "roles": {
                            "L": [
                                {"S": "Data Engineer"},
                                {"S": "Developer/Engineer"},
                                {"S": "IT Administrator"},
                            ]
                        },
                        "scheduleUid": {"S": "A7956934-FF28-473D-96A8-012D497C6716"},
                        "description": {
                            "S": "Amazon EC2 Auto Scaling groups empower users to benefit from the elasticity benefits of the AWS Cloud. In this workshop, learn how you can make the most of the latest innovations from EC2 Auto Scaling to improve your web application availability at lower costs. Specifically, find out how to use a combination of predictive scaling, dynamic scaling, and warm pool features to automatically launch and terminate capacity with changing demands. With more responsive and proactive scaling, you run only the required number of instances at any time of the day, reducing the cost of overprovisioned EC2 instances. You must bring your laptop to participate."
                        },
                        "services": {
                            "L": [
                                {"S": "Amazon EC2 Auto Scaling"},
                                {"S": "Amazon Elastic Compute Cloud (EC2)"},
                            ]
                        },
                        "trackName": {"S": "updated track name"},
                        "title": {
                            "S": "Proactive auto scaling for optimal cost and availability"
                        },
                        "tags": {
                            "L": [
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "CCEE8B58-D74C-4469-8FE4-19F0C692CC6C"
                                        },
                                        "parentTagUid": {
                                            "S": "7A26869A-A0C9-48CC-9731-541C3AFA9DF4"
                                        },
                                        "tagName": {"S": "Amazon EC2 Auto Scaling"},
                                        "parentTagName": {"S": "Services"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "7807988D-1640-44DE-B5D4-CAB4A3D98CC1"
                                        },
                                        "parentTagUid": {
                                            "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                        },
                                        "tagName": {"S": "Data Engineer"},
                                        "parentTagName": {"S": "Role"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "4F085EF2-7954-4A96-9A8C-45BC0EC61359"
                                        },
                                        "parentTagUid": {
                                            "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                        },
                                        "tagName": {"S": "Developer/Engineer"},
                                        "parentTagName": {"S": "Role"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "DE0F6885-27E7-4BAC-AB2C-A234A7F6BCCB"
                                        },
                                        "parentTagUid": {
                                            "S": "F2BB2A9C-8783-4072-A0A4-5621D1A481A6"
                                        },
                                        "tagName": {"S": "Compute"},
                                        "parentTagName": {"S": "Topic"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "F42B9C9D-C9B8-4399-8F91-658AAA167ED9"
                                        },
                                        "parentTagUid": {
                                            "S": "B78A961D-DC03-42C9-A32E-DA576734A89E"
                                        },
                                        "tagName": {"S": "Cross Industry "},
                                        "parentTagName": {"S": "Industry"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "B2CA25EB-C2BD-42B2-9FC5-0B607ACD4C19"
                                        },
                                        "parentTagUid": {
                                            "S": "7A26869A-A0C9-48CC-9731-541C3AFA9DF4"
                                        },
                                        "tagName": {
                                            "S": "Amazon Elastic Compute Cloud (EC2)"
                                        },
                                        "parentTagName": {"S": "Services"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "B6C0FC98-BE24-4ABB-8B2C-939AF5F58363"
                                        },
                                        "parentTagUid": {
                                            "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                        },
                                        "tagName": {"S": "IT Administrator"},
                                        "parentTagName": {"S": "Role"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "20445AB2-C0C4-4DE2-9443-F1B9780A69CE"
                                        },
                                        "parentTagUid": {
                                            "S": "3428EB86-4D79-4EFE-9F33-E911FCC500A4"
                                        },
                                        "tagName": {"S": "Migration & Transfer"},
                                        "parentTagName": {"S": "Area of Interest"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "594D1AC5-4EDB-442A-BD5E-EE580E43441E"
                                        },
                                        "parentTagUid": {
                                            "S": "3428EB86-4D79-4EFE-9F33-E911FCC500A4"
                                        },
                                        "tagName": {"S": "Cost Optimization"},
                                        "parentTagName": {"S": "Area of Interest"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "6F2C43D3-196B-4957-82C5-9F46BAC3DE5E"
                                        },
                                        "parentTagUid": {
                                            "S": "2634F5B6-B8E0-4208-92C3-FAE426C930F7"
                                        },
                                        "tagName": {"S": "400 - Expert"},
                                        "parentTagName": {"S": "Level"},
                                    }
                                },
                            ]
                        },
                        "thirdPartyID": {"S": "CMP403"},
                        "industries": {"L": [{"S": "Cross Industry"}]},
                        "sessionUid": {"S": "E32C1CD6-D674-4966-B1EA-8E5D082F906F"},
                        "SK": {"S": "CMP403"},
                        "sessionType": {"S": "Workshop"},
                        "scheduleTrackUid": {
                            "S": "5F87F61B-CEE9-ED11-81DB-A4AC1C44CA4E"
                        },
                        "PK": {"S": "ReInventSession"},
                        "areas_of_interest": {
                            "L": [
                                {"S": "Migration & Transfer"},
                                {"S": "Cost Optimization"},
                            ]
                        },
                    },
                    "OldImage": {
                        "level": {"N": "400"},
                        "topics": {"L": [{"S": "Compute"}]},
                        "roles": {
                            "L": [
                                {"S": "Data Engineer"},
                                {"S": "Developer/Engineer"},
                                {"S": "IT Administrator"},
                            ]
                        },
                        "scheduleUid": {"S": "A7956934-FF28-473D-96A8-012D497C6716"},
                        "description": {
                            "S": "Amazon EC2 Auto Scaling groups empower users to benefit from the elasticity benefits of the AWS Cloud. In this workshop, learn how you can make the most of the latest innovations from EC2 Auto Scaling to improve your web application availability at lower costs. Specifically, find out how to use a combination of predictive scaling, dynamic scaling, and warm pool features to automatically launch and terminate capacity with changing demands. With more responsive and proactive scaling, you run only the required number of instances at any time of the day, reducing the cost of overprovisioned EC2 instances. You must bring your laptop to participate."
                        },
                        "services": {
                            "L": [
                                {"S": "Amazon EC2 Auto Scaling"},
                                {"S": "Amazon Elastic Compute Cloud (EC2)"},
                            ]
                        },
                        "trackName": {"S": "Workshop"},
                        "title": {
                            "S": "Proactive auto scaling for optimal cost and availability"
                        },
                        "tags": {
                            "L": [
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "CCEE8B58-D74C-4469-8FE4-19F0C692CC6C"
                                        },
                                        "parentTagUid": {
                                            "S": "7A26869A-A0C9-48CC-9731-541C3AFA9DF4"
                                        },
                                        "tagName": {"S": "Amazon EC2 Auto Scaling"},
                                        "parentTagName": {"S": "Services"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "7807988D-1640-44DE-B5D4-CAB4A3D98CC1"
                                        },
                                        "parentTagUid": {
                                            "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                        },
                                        "tagName": {"S": "Data Engineer"},
                                        "parentTagName": {"S": "Role"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "4F085EF2-7954-4A96-9A8C-45BC0EC61359"
                                        },
                                        "parentTagUid": {
                                            "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                        },
                                        "tagName": {"S": "Developer/Engineer"},
                                        "parentTagName": {"S": "Role"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "DE0F6885-27E7-4BAC-AB2C-A234A7F6BCCB"
                                        },
                                        "parentTagUid": {
                                            "S": "F2BB2A9C-8783-4072-A0A4-5621D1A481A6"
                                        },
                                        "tagName": {"S": "Compute"},
                                        "parentTagName": {"S": "Topic"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "F42B9C9D-C9B8-4399-8F91-658AAA167ED9"
                                        },
                                        "parentTagUid": {
                                            "S": "B78A961D-DC03-42C9-A32E-DA576734A89E"
                                        },
                                        "tagName": {"S": "Cross Industry "},
                                        "parentTagName": {"S": "Industry"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "B2CA25EB-C2BD-42B2-9FC5-0B607ACD4C19"
                                        },
                                        "parentTagUid": {
                                            "S": "7A26869A-A0C9-48CC-9731-541C3AFA9DF4"
                                        },
                                        "tagName": {
                                            "S": "Amazon Elastic Compute Cloud (EC2)"
                                        },
                                        "parentTagName": {"S": "Services"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "B6C0FC98-BE24-4ABB-8B2C-939AF5F58363"
                                        },
                                        "parentTagUid": {
                                            "S": "22A77ABD-348D-4E44-800F-846017E75A5D"
                                        },
                                        "tagName": {"S": "IT Administrator"},
                                        "parentTagName": {"S": "Role"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "20445AB2-C0C4-4DE2-9443-F1B9780A69CE"
                                        },
                                        "parentTagUid": {
                                            "S": "3428EB86-4D79-4EFE-9F33-E911FCC500A4"
                                        },
                                        "tagName": {"S": "Migration & Transfer"},
                                        "parentTagName": {"S": "Area of Interest"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "594D1AC5-4EDB-442A-BD5E-EE580E43441E"
                                        },
                                        "parentTagUid": {
                                            "S": "3428EB86-4D79-4EFE-9F33-E911FCC500A4"
                                        },
                                        "tagName": {"S": "Cost Optimization"},
                                        "parentTagName": {"S": "Area of Interest"},
                                    }
                                },
                                {
                                    "M": {
                                        "scheduleTagUid": {
                                            "S": "6F2C43D3-196B-4957-82C5-9F46BAC3DE5E"
                                        },
                                        "parentTagUid": {
                                            "S": "2634F5B6-B8E0-4208-92C3-FAE426C930F7"
                                        },
                                        "tagName": {"S": "400 - Expert"},
                                        "parentTagName": {"S": "Level"},
                                    }
                                },
                            ]
                        },
                        "thirdPartyID": {"S": "CMP403"},
                        "industries": {"L": [{"S": "Cross Industry"}]},
                        "sessionUid": {"S": "E32C1CD6-D674-4966-B1EA-8E5D082F906F"},
                        "SK": {"S": "CMP403"},
                        "sessionType": {"S": "Workshop"},
                        "scheduleTrackUid": {
                            "S": "5F87F61B-CEE9-ED11-81DB-A4AC1C44CA4E"
                        },
                        "PK": {"S": "ReInventSession"},
                        "areas_of_interest": {
                            "L": [
                                {"S": "Migration & Transfer"},
                                {"S": "Cost Optimization"},
                            ]
                        },
                    },
                    "SequenceNumber": "17525800000000051698704652",
                    "SizeBytes": 5447,
                    "StreamViewType": "NEW_AND_OLD_IMAGES",
                },
                "eventSourceARN": "arn:aws:dynamodb:eu-west-1:739178438747:table/ReInventSessionTable/stream/2023-08-05T21:30:53.861",
            },
        ]
    }
    handler(event, None)
