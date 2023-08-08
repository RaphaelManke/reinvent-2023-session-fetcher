from aws_cdk import (
    Duration,
    aws_dynamodb as dynamodb,
    aws_events as events,
    aws_events_targets as targets,
    aws_lambda as lambda_,
)
from constructs import Construct


class DdbUpdateWriter(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        ddb_table: dynamodb.Table,
        event_bus: events.EventBus,
        common_layer: lambda_.LayerVersion,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        function = lambda_.Function(
            scope=self,
            id="DdbUpdateFunction",
            code=lambda_.Code.from_asset("resources/functions/ddb_updater"),
            handler="index.handler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            architecture=lambda_.Architecture.X86_64,
            layers=[common_layer],
            environment={
                "DDB_TABLE_NAME": ddb_table.table_name,
                "POWERTOOLS_SERVICE_NAME": "reinvent2023_session_fetcher",
                "LOG_LEVEL": "INFO",
                "EVENT_BUS_NAME": event_bus.event_bus_name,
            },
            memory_size=1024,
            timeout=Duration.seconds(30),
        )
        ddb_table.grant_write_data(function)

        events.Rule(
            scope=self,
            id="DdbUpdateRule",
            event_bus=event_bus,
            targets=[targets.LambdaFunction(handler=function)],
            event_pattern=events.EventPattern(
                source=["ReInventSessionFetcher"],
                detail_type=[
                    "SessionAdded",
                    "SessionUpdated",
                    "SessionRemoved",
                ],
            ),
        )
