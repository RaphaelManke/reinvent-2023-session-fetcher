from decimal import Decimal
from typing import List, Optional, Dict
import boto3
import json
import re
from deepdiff import DeepDiff
from boto3.dynamodb.types import TypeDeserializer

from models import (
    ReInventSession,
    ReInventSessionListDiff,
    ReInventSessionDiff,
    ReInventSessionFieldDiff,
)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)  # Convert Decimal to string representation
        return super(DecimalEncoder, self).default(o)


class SessionController:
    def __init__(self, db_table_name: str):
        self._db_table_name = db_table_name
        self._ddb_client = boto3.client("dynamodb")
        self._ddb_resource = boto3.resource("dynamodb")
        self._deserializer = TypeDeserializer()

        self._table = self._ddb_resource.Table(self._db_table_name)
        self.sessions = self._init_from_db()

    def _init_from_db(self) -> List[ReInventSession]:
        """Load all sessions from the database"""
        paginator = self._ddb_client.get_paginator("query")
        response_iterator = paginator.paginate(
            TableName=self._db_table_name,
            KeyConditionExpression=f"#pk = :val",
            ExpressionAttributeNames={"#pk": "PK"},
            ExpressionAttributeValues={":val": {"S": "ReInventSession"}},
        )

        session_list = []
        # Iterate through the paginated results
        for page in response_iterator:
            items = page["Items"]
            # Do something with the items returned (e.g., print them)
            for item in items:
                deserialized_item = {
                    key: self._deserializer.deserialize(value)
                    for key, value in item.items()
                }

                session_list.append(ReInventSession(**deserialized_item))
        return session_list

    def insert_new_sessions(self, new_session_list: List[ReInventSession]):
        """Insert new sessions into the database"""
        # Use the DDB batch write API to insert new sessions

        for session in new_session_list:
            item_data = {
                "PK": "ReInventSession",
                "SK": session.sessionUid,
            } | session.model_dump()

            # Add a condition expression to prevent overwriting existing items
            condition_expression = (
                "attribute_not_exists(PK) AND attribute_not_exists(SK)"
            )

            try:
                self._table.put_item(
                    Item=item_data, ConditionExpression=condition_expression
                )
            except self._table.meta.client.exceptions.ConditionalCheckFailedException:
                # Handle the case when the item already exists (ConditionalCheckFailedException)
                print(
                    f"Item with PK: ReInventSession and SK: {session.sessionUid} already exists."
                )

    def update_sessions(self, updated_session_list: List[ReInventSession]):
        """Update sessions in the database"""
        for session in updated_session_list:
            item_data = {
                "PK": "ReInventSession",
                "SK": session.sessionUid,
            } | session.model_dump()

            self._table.put_item(Item=item_data)

    def remove_sessions(self, session_list: List[ReInventSession]):
        """Insert new sessions into the database"""
        # Use the DDB batch write API to insert new sessions
        for session in session_list:
            self._table.delete_item(
                Key={
                    "PK": "ReInventSession",
                    "SK": session.sessionUid,
                }
            )

    def generate_diff(
        self, new_session_list: List[ReInventSession]
    ) -> ReInventSessionListDiff:
        """Generate a diff between the current sessions and the new ones."""
        added_sessions: Dict[str, ReInventSession] = {}
        removed_sessions: Dict[str, ReInventSession] = {}
        updated_sessions: Dict[str, ReInventSessionDiff] = {}
        not_updated_sessions: List[str] = []

        old_sessions_map = {session.sessionUid: session for session in self.sessions}

        # If a session from the database is not present in the new list, it is removed
        for old_session_id in old_sessions_map:
            if old_session_id not in [
                session.sessionUid for session in new_session_list
            ]:
                # Add it to the list of removed sessions
                removed_sessions[old_session_id] = old_sessions_map[old_session_id]
                print(
                    f"Session {old_session_id} ({old_sessions_map[old_session_id].thirdPartyID}) is removed"
                )

        for new_session in new_session_list:
            # If a new session is not present in the old list, it is added
            if new_session.sessionUid not in old_sessions_map:
                # Add it to the list of added sessions
                added_sessions[new_session.sessionUid] = new_session
                print(
                    f"Session {new_session.sessionUid} ({new_session.thirdPartyID}) is added"
                )

            # If a session is present in both lists, it might be updated
            if new_session.sessionUid in old_sessions_map:
                # Check if there are differences between the old session and the new one
                session_field_diff = self.get_session_diff(
                    session_a=old_sessions_map[new_session.sessionUid],
                    session_b=new_session,
                )

                # If there are differences, add the session to the list of updated sessions,
                # including the differences found.
                if session_field_diff:
                    updated_sessions[new_session.sessionUid] = ReInventSessionDiff(
                        old_session=old_sessions_map[new_session.sessionUid],
                        new_session=new_session,
                        changed_fields=session_field_diff,
                    )
                    print(
                        f"Session {new_session.sessionUid} ({new_session.thirdPartyID}) is updated"
                    )
                else:
                    not_updated_sessions.append(new_session.sessionUid)

        print(f"Found {len(not_updated_sessions)} sessions without changes")

        return ReInventSessionListDiff(
            added_sessions=added_sessions,
            removed_sessions=removed_sessions,
            updated_sessions=updated_sessions,
        )

    def get_session_diff(
        self, session_a: ReInventSession, session_b: ReInventSession
    ) -> List[ReInventSessionFieldDiff]:
        session_a_dump = session_a.model_dump()
        session_b_dump = session_b.model_dump()

        diff = DeepDiff(
            session_a_dump,
            session_b_dump,
            ignore_order=True,
            verbose_level=1,
        )
        if not diff:
            return []

        changes = []
        for key in diff.keys():
            key_regex = r"root\[\'(.*?)\'\].*"
            match = re.match(key_regex, key)

            for diff_type in diff[key]:
                match = re.match(key_regex, diff_type)
                if match:
                    changed_key = match[1]
                    changes.append(
                        ReInventSessionFieldDiff(
                            field=changed_key,
                            old_value=session_a_dump.get(changed_key),
                            new_value=session_b_dump.get(changed_key),
                        )
                    )

        return changes

    @staticmethod
    def get_session_from_list_by_id(
        session_id: str, session_list: List[ReInventSession]
    ) -> Optional[ReInventSession]:
        """Get a session from a list of sessions, given its ID."""
        for session in session_list:
            if session.sessionUid == session_id:
                return session
        return None

    def get_session_by_id(self, session_id: str) -> Optional[ReInventSession]:
        """Get a session from a list of sessions, given its ID."""
        for session in self.sessions:
            if session.sessionUid == session_id:
                return session
        return None
