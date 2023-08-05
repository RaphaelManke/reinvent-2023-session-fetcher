from typing import List, Optional, Dict
import boto3
from boto3.dynamodb.types import TypeDeserializer

from models import (
    ReInventSession,
    ReInventSessionListDiff,
    ReInventSessionDiff,
    ReInventSessionFieldDiff,
)


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

                session_list.append(
                    ReInventSession.model_construct(**deserialized_item)
                )
        return session_list

    def insert_new_sessions(self, new_session_list: List[ReInventSession]):
        """Insert new sessions into the database"""
        # Use the DDB batch write API to insert new sessions

        for session in new_session_list:
            item_data = {
                "PK": "ReInventSession",
                "SK": session.session_id,
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
                    f"Item with PK: ReInventSession and SK: {session.session_id} already exists."
                )

    def remove_sessions(self, session_list: List[ReInventSession]):
        """Insert new sessions into the database"""
        # Use the DDB batch write API to insert new sessions
        for session in session_list:
            self._table.delete_item(
                Key={
                    "PK": "ReInventSession",
                    "SK": session.session_id,
                }
            )

    def generate_diff(
        self, new_session_list: List[ReInventSession]
    ) -> ReInventSessionListDiff:
        """Generate a diff between the current sessions and the new ones."""
        added_sessions: Dict[str, ReInventSession] = {}
        removed_sessions: Dict[str, ReInventSession] = {}
        updated_sessions: Dict[str, ReInventSessionDiff] = {}

        old_sessions_map = {session.session_id: session for session in self.sessions}

        # If a session from the database is not present in the new list, it is removed
        for old_session_id in old_sessions_map:
            if old_session_id not in [
                session.session_id for session in new_session_list
            ]:
                # Add it to the list of removed sessions
                removed_sessions[old_session_id] = old_sessions_map[old_session_id]
                print(f"Session {old_session_id} is removed")

        for new_session in new_session_list:
            # If a new session is not present in the old list, it is added
            if new_session.session_id not in old_sessions_map:
                # Add it to the list of added sessions
                added_sessions[new_session.session_id] = new_session
                print(f"Session {new_session.session_id} is added")

            # If a session is present in both lists, it might be updated
            if new_session.session_id in old_sessions_map:
                # Check if there are differences between the old session and the new one
                session_field_diff = self.get_session_diff(
                    session_a=self.get_session_by_id(new_session.session_id),
                    session_b=old_sessions_map[new_session.session_id],
                )

                # If there are differences, add the session to the list of updated sessions,
                # including the differences found.
                if session_field_diff:
                    updated_sessions[new_session.session_id] = ReInventSessionDiff(
                        old_session=old_sessions_map[new_session.session_id],
                        new_session=new_session,
                        changed_fields=session_field_diff,
                    )
                    print(f"Session {new_session.session_id} is updated")
                else:
                    print(f"Session {new_session.session_id} is not updated")

        return ReInventSessionListDiff(
            added_sessions=added_sessions,
            removed_sessions=removed_sessions,
            updated_sessions=updated_sessions,
        )

    @staticmethod
    def get_session_diff(
        session_a: ReInventSession, session_b: ReInventSession
    ) -> List[ReInventSessionFieldDiff]:
        return []

    @staticmethod
    def get_session_from_list_by_id(
        session_id: str, session_list: List[ReInventSession]
    ) -> Optional[ReInventSession]:
        """Get a session from a list of sessions, given its ID."""
        for session in session_list:
            if session.session_id == session_id:
                return session
        return None

    def get_session_by_id(self, session_id: str) -> Optional[ReInventSession]:
        """Get a session from a list of sessions, given its ID."""
        for session in self.sessions:
            if session.session_id == session_id:
                return session
        return None
