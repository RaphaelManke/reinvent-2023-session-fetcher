from aws_cdk import (
    Duration,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_lambda as lambda_,
)
from constructs import Construct


class FetcherTrigger(Construct):
    def __init__(
        self, scope: Construct, id: str, fetcher_lambda: lambda_.Function, **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # Create a Rule to trigger the Fetcher Lambda
        rule = events.Rule(
            scope=self,
            id="Rule",
            schedule=events.Schedule.rate(Duration.minutes(5)),
            targets=[
                events_targets.LambdaFunction(
                    handler=fetcher_lambda,
                )
            ],
        )
