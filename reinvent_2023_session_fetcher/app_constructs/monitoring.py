from cdk_monitoring_constructs import (
    MonitoringFacade,
    ErrorCountThreshold,
    SnsAlarmActionStrategy,
)
from constructs import Construct
from aws_cdk import (
    aws_lambda as lambda_,
    aws_sns as sns,
    aws_chatbot as chatbot,
)


class Monitoring(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        fetcherLambda: lambda_.Function,
        slackNotifierLambda: lambda_.Function,
        slack_workspace_id: str,
        slack_channel_id: str,
        slack_channel_configuration_name: str,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        chatbotTopic = sns.Topic(scope=self, id="ChatbotTopic")
        slackChannel = chatbot.SlackChannelConfiguration(
            scope=self,
            id="ChatbotSlackChannel",
            slack_channel_configuration_name=slack_channel_configuration_name,
            slack_workspace_id=slack_workspace_id,
            slack_channel_id=slack_channel_id,
        )

        slackChannel.add_notification_topic(notification_topic=chatbotTopic)

        monitoring = MonitoringFacade(
            scope=self,
            id="Monitoring",
            alarm_factory_defaults={
                "actions_enabled": True,
                "alarm_name_prefix": "ReInventSessions",
                "action": SnsAlarmActionStrategy(
                    on_alarm_topic=chatbotTopic,
                    on_ok_topic=chatbotTopic,
                ),
            },
        )

        monitoring.monitor_lambda_function(
            lambda_function=fetcherLambda,
            add_fault_count_alarm={
                "Warning": ErrorCountThreshold(
                    max_error_count=1,
                )
            },
        )

        monitoring.monitor_lambda_function(
            lambda_function=slackNotifierLambda,
            add_fault_count_alarm={
                "Warning": ErrorCountThreshold(
                    max_error_count=1,
                )
            },
        )
