from aws_cdk import (
    aws_events as events,
    aws_scheduler as scheduler,
)
from constructs import Construct


class Messaging(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        fetcher_schedule: scheduler.CfnSchedule,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # Create an Event Bus
        self.event_bus = events.EventBus(
            scope=self,
            id="ReInventSessionsEventBus",
            event_bus_name="ReInventSessionsEventBus",
        )

        # Don't start the scheduler before the Event Bus is ready.
        fetcher_schedule.add_dependency(self.event_bus.node.default_child)
