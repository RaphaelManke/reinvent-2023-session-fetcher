from aws_cdk import (
    aws_events as events,
)
from constructs import Construct


class Messaging(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create an Event Bus
        self.event_bus = events.EventBus(
            scope=self,
            id="ReInventSessionsEventBus",
            event_bus_name="ReInventSessionsEventBus",
        )
