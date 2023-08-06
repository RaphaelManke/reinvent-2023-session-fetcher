from aws_cdk import (
    Duration,
    RemovalPolicy,
    aws_lambda as lambda_,
    aws_lambda_event_sources as lambda_event_sources,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_sqs as sqs,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct


class SlackNotifier(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        event_bus: events.EventBus,
        common_layer: lambda_.LayerVersion,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)
        slack_webhook_url_secret = secretsmanager.Secret(
            scope=self,
            id="SlackWebhookUrlSecret",
            removal_policy=RemovalPolicy.DESTROY,
        )
        queue = sqs.Queue(
            scope=self,
            id="SlackNotifierInputQueue",
            retention_period=Duration.days(2),
        )
        # Create a eventbus rule that match events with source "ReInventSessionFetcher" and detaul-type one of "SessionAdded", "SessionUpdated" or "SessionRemoved"
        # The target of the rule is the SlackNotifierInputQueue
        rule = events.Rule(
            scope=self,
            id="SessionEventRule",
            event_bus=event_bus,
            event_pattern=events.EventPattern(
                source=["ReInventSessionFetcher"],
                detail_type=[
                    "SessionAdded",
                    "SessionUpdated",
                    "SessionRemoved",
                ],
            ),
            targets=[events_targets.SqsQueue(queue=queue)],
        )

        self.function = lambda_.Function(
            scope=self,
            id="SlackNotifierFunction",
            code=lambda_.Code.from_asset("resources/functions/slack_notifier"),
            handler="index.handler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            architecture=lambda_.Architecture.X86_64,
            layers=[common_layer],
            environment={
                "POWERTOOLS_SERVICE_NAME": "reinvent2023_session_slack_notifier",
                "LOG_LEVEL": "INFO",
                "SLACK_WEBHOOK_URL_SECRET_NAME": slack_webhook_url_secret.secret_name,
            },
            memory_size=1024,
            timeout=Duration.seconds(30),
        )

        self.function.add_event_source(
            source=lambda_event_sources.SqsEventSource(queue=queue, batch_size=1)
        )
        slack_webhook_url_secret.grant_read(self.function)
