from aws_cdk import (
    Duration,
    aws_scheduler as scheduler,
    aws_events as events,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class EventGenerator(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        ddb_table: dynamodb.Table,
        event_bus: events.EventBus,
        common_layer: lambda_.LayerVersion,
        fetcher_schedule: scheduler.CfnSchedule,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        function = lambda_.Function(
            scope=self,
            id="EventGeneratorFunction",
            code=lambda_.Code.from_asset("resources/functions/event_generator"),
            handler="index.handler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            architecture=lambda_.Architecture.X86_64,
            layers=[common_layer],
            environment={
                "EVENT_BUS_NAME": event_bus.event_bus_name,
            },
            memory_size=1024,
            timeout=Duration.seconds(30),
        )
        function.add_event_source_mapping(
            id="DynamoDBMapping",
            event_source_arn=ddb_table.table_stream_arn,
            starting_position=lambda_.StartingPosition.LATEST,
            filters=[  # Only trigger on changes to 'ReInventSession' items
                lambda_.FilterCriteria.filter(
                    {"dynamodb": {"Keys": {"PK": {"S": ["ReInventSession"]}}}}
                )
            ],
        )

        event_bus.grant_all_put_events(function)
        ddb_table.grant_stream_read(function)

        # Don't start the scheduler before the EventGeneratorFunction is ready.
        fetcher_schedule.add_dependency(function.node.default_child)
