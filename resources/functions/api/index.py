from decimal import Decimal
from http import HTTPStatus
from typing import List, Dict
import boto3
import json
import os
from aws_lambda_powertools.utilities.typing import LambdaContext
from boto3.dynamodb.types import TypeDeserializer

from aws_lambda_powertools.event_handler import (
    APIGatewayRestResolver,
    Response,
    content_types,
    CORSConfig,
)

DDB_TABLE_NAME = os.environ["DDB_TABLE_NAME"]


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)  # Convert Decimal to string representation
        return super(DecimalEncoder, self).default(o)


app = APIGatewayRestResolver()
cors_config = CORSConfig(allow_origin="*", max_age=300)
app = APIGatewayRestResolver(cors=cors_config)

ddb_client = boto3.client("dynamodb")
type_deserializer = TypeDeserializer()


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    response = app.resolve(event, context)
    return response


@app.get("/sessions")
def get_sessions() -> Response:
    payload = _get_all_sessions()
    return Response(
        status_code=HTTPStatus.OK,
        content_type=content_types.APPLICATION_JSON,
        body=json.dumps(payload, cls=DecimalEncoder),
        compress=True,
    )


@app.get("/sessions/<session_id>")
def get_session(session_id: str) -> Response:
    try:
        payload = _get_session(session_id)
        return Response(
            status_code=HTTPStatus.OK,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps(payload, cls=DecimalEncoder),
            compress=True,
        )
    except Exception as exc:
        print(f"Error: {type(exc).__name__} - {exc}")
        return Response(
            status_code=HTTPStatus.NOT_FOUND,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps({"error": "Session not found"}, cls=DecimalEncoder),
            compress=True,
        )


@app.get("/sessions/<session_id>/history")
def get_session(session_id) -> Response:
    payload = _get_session_history(session_id)

    # sort payload by mutation date, descending
    nested_key = lambda x: x["SK"]
    sorted_data = sorted(payload, key=nested_key, reverse=True)

    return Response(
        status_code=HTTPStatus.OK,
        content_type=content_types.APPLICATION_JSON,
        body=json.dumps(sorted_data, cls=DecimalEncoder),
        compress=True,
    )


@app.get("/mutations")
def get_mutations() -> Response:
    payload = _get_all_mutations()
    return Response(
        status_code=HTTPStatus.OK,
        content_type=content_types.APPLICATION_JSON,
        body=json.dumps(payload, cls=DecimalEncoder),
        compress=True,
    )


def _get_all_sessions() -> List:
    """Load all sessions from the database"""
    paginator = ddb_client.get_paginator("query")
    response_iterator = paginator.paginate(
        TableName=DDB_TABLE_NAME,
        KeyConditionExpression=f"#pk = :val",
        ExpressionAttributeNames={"#pk": "PK"},
        ExpressionAttributeValues={":val": {"S": "ReInventSession"}},
    )
    return _deserialize_list(response_iterator)


def _get_session(session_id: str) -> Dict:
    """Load a single session from the database"""
    response = ddb_client.query(
        TableName=DDB_TABLE_NAME,
        KeyConditionExpression="#pk = :pkval AND #sk = :skval",
        ExpressionAttributeNames={
            "#pk": "PK",
            "#sk": "SK",
        },
        ExpressionAttributeValues={
            ":pkval": {"S": "ReInventSession"},
            ":skval": {"S": session_id},
        },
        Limit=1,  # Limit the result to return only one item
    )

    try:
        item = response["Items"][0]  # Retrieve the single item from the response
        deserialized_item = {
            key: type_deserializer.deserialize(value) for key, value in item.items()
        }
        return deserialized_item

    except Exception as exc:
        print(f"Failed to retrieve item: {type(exc).__name__}: {str(exc)}")
        raise RuntimeError(f"Session {session_id} not found")


def _get_session_history(session_id) -> List:
    """Load the history of a single session from the database"""
    paginator = ddb_client.get_paginator("query")
    response_iterator = paginator.paginate(
        TableName=DDB_TABLE_NAME,
        KeyConditionExpression=f"#pk = :val",
        ExpressionAttributeNames={"#pk": "PK"},
        ExpressionAttributeValues={":val": {"S": f"{session_id}#SessionMutation"}},
    )
    return _deserialize_list(response_iterator)


def _get_all_mutations() -> List:
    """Load all mutations from the database"""
    paginator = ddb_client.get_paginator("query")
    response_iterator = paginator.paginate(
        TableName=DDB_TABLE_NAME,
        KeyConditionExpression=f"#pk = :val",
        ExpressionAttributeNames={"#pk": "PK"},
        ExpressionAttributeValues={":val": {"S": "SessionMutation"}},
    )
    return _deserialize_list(response_iterator)


def _deserialize_list(response_iterator):
    item_list = []
    # Iterate through the paginated results
    for page in response_iterator:
        items = page.get("Items")
        if not items:
            continue
        # Deserialize all DDB items
        for item in items:
            deserialized_item = {
                key: type_deserializer.deserialize(value) for key, value in item.items()
            }

            item_list.append(deserialized_item)
    return item_list
