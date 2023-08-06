from aws_cdk import Stack
from constructs import Construct
from reinvent_2023_session_fetcher.app_constructs.slack_notifier import SlackNotifier

from reinvent_2023_session_fetcher.app_constructs.storage import Storage
from reinvent_2023_session_fetcher.app_constructs.fetcher import Fetcher
from reinvent_2023_session_fetcher.app_constructs.event_generator import EventGenerator
from reinvent_2023_session_fetcher.app_constructs.messaging import Messaging


class Reinvent2023SessionFetcherStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        storage = Storage(
            scope=self,
            id="Storage",
        )

        Fetcher(
            scope=self,
            id="Fetcher",
            credential_secret=storage.credentials_secret,
            ddb_table=storage.table,
            common_layer=storage.common_layer,
        )

        messaging = Messaging(
            scope=self,
            id="Messaging",
        )

        EventGenerator(
            scope=self,
            id="EventGenerator",
            ddb_table=storage.table,
            event_bus=messaging.event_bus,
            common_layer=storage.common_layer,
        )

        SlackNotifier(
            scope=self,
            id="SlackNotifier",
            event_bus=messaging.event_bus,
            common_layer=storage.common_layer,
        )
