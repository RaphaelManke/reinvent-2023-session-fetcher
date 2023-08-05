from aws_cdk import Stack
from constructs import Construct

from reinvent_2023_session_fetcher.app_constructs.storage import Storage
from reinvent_2023_session_fetcher.app_constructs.fetcher import Fetcher


class Reinvent2023SessionFetcherStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        storage = Storage(
            scope=self,
            id="Storage",
        )

        Fetcher(scope=self, id="Fetcher", credential_secret=storage.credentials_secret)

        # EventGenerator()
