from aws_lambda_powertools.utilities.typing import LambdaContext
from boto3.dynamodb.types import TypeDeserializer
from copy import deepcopy
from decimal import Decimal
from http import HTTPStatus
from typing import List, Dict, Union
import boto3
import json
import os

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

    # Sort payload by session id, ascending
    sorted_data = _sort_list_by_nested_key(
        source_list=payload, nested_key="SK", reverse=False
    )
    _purge_ddb_pk_and_sk(sorted_data)

    response = {"sessions": sorted_data}
    return Response(
        status_code=HTTPStatus.OK,
        content_type=content_types.APPLICATION_JSON,
        body=json.dumps(response, cls=DecimalEncoder),
        compress=True,
    )


@app.get("/sessions/<session_id>")
def get_session(session_id: str) -> Response:
    try:
        payload = _get_session(session_id)
        _purge_ddb_pk_and_sk(payload)

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
def get_session_history(session_id) -> Response:
    payload = _get_session_history(session_id)
    cleaned_mutations = _sort_and_clean_mutations(payload)
    for mutation in cleaned_mutations:
        _purge_ddb_pk_and_sk(mutation)
        _purge_ddb_pk_and_sk(mutation["mutationData"])

    response = {"mutations": cleaned_mutations}
    return Response(
        status_code=HTTPStatus.OK,
        content_type=content_types.APPLICATION_JSON,
        body=json.dumps(response, cls=DecimalEncoder),
        compress=True,
    )


@app.get("/mutations")
def get_mutations() -> Response:
    payload = _get_all_mutations()
    cleaned_mutations = _sort_and_clean_mutations(payload)

    for mutation in cleaned_mutations:
        _purge_ddb_pk_and_sk(mutation)
        _purge_ddb_pk_and_sk(mutation["mutationData"])
        if "new" in mutation["mutationData"]:
            _purge_ddb_pk_and_sk(mutation["mutationData"]["new"])
        if "old" in mutation["mutationData"]:
            _purge_ddb_pk_and_sk(mutation["mutationData"]["old"])

    response = {"mutations": cleaned_mutations}
    return Response(
        status_code=HTTPStatus.OK,
        content_type=content_types.APPLICATION_JSON,
        body=json.dumps(response, cls=DecimalEncoder),
        compress=True,
    )


def _sort_and_clean_mutations(mutations: List) -> List:
    """Sort mutations by timestamp, and remove unnecessary keys"""

    # Sort payload by mutation date, descending
    sorted_data = _sort_list_by_nested_key(
        source_list=mutations, nested_key="SK", reverse=True
    )
    # Set the mutationDateTime field
    for item in sorted_data:
        item["mutationDateTime"] = item["SK"]

    return sorted_data


def _purge_ddb_pk_and_sk(data: Union[List, Dict]) -> None:
    """Remove keys from the response that are not needed"""
    if isinstance(data, list):
        for item in data:
            item.pop("PK", None)
            item.pop("SK", None)
    elif isinstance(data, dict):
        data.pop("PK", None)
        data.pop("SK", None)


def _sort_list_by_nested_key(source_list, nested_key, reverse=False):
    """Sort a list of dictionaries by a nested key"""
    if not isinstance(source_list, list):
        raise TypeError(f"Can only sort lists, not {type(source_list)}")

    try:
        nested_key_getter = lambda x: x[nested_key]
        sorted_data = sorted(source_list, key=nested_key_getter, reverse=reverse)
    except Exception as exc:
        print(f"Failed to sort list: {type(exc).__name__}: {str(exc)}")
        return source_list

    return sorted_data


def _get_all_sessions() -> List:
    """Load all sessions from the database"""
    paginator = ddb_client.get_paginator("query")
    response_iterator = paginator.paginate(
        TableName=DDB_TABLE_NAME,
        KeyConditionExpression=f"#pk = :val",
        ExpressionAttributeNames={"#pk": "PK"},
        ExpressionAttributeValues={":val": {"S": "ReInventSession"}},
    )
    return _deserialize_ddb_query_paginator(response_iterator)


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
    return _deserialize_ddb_query_paginator(response_iterator)


def _get_all_mutations() -> List:
    """Load all mutations from the database"""
    paginator = ddb_client.get_paginator("query")
    response_iterator = paginator.paginate(
        TableName=DDB_TABLE_NAME,
        KeyConditionExpression=f"#pk = :val",
        ExpressionAttributeNames={"#pk": "PK"},
        ExpressionAttributeValues={":val": {"S": "SessionMutation"}},
    )
    response_list = _deserialize_ddb_query_paginator(response_iterator)
    for item in response_list:
        session_title = None
        if item["mutationType"] == "SessionUpdated":
            session_title = item["mutationData"]["new"]["title"]
        else:
            session_title = item["mutationData"]["title"]

        item["sessionTitle"] = session_title
        print(session_title)

    return response_list


def _deserialize_ddb_query_paginator(response_iterator):
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
