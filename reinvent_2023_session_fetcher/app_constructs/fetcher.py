from aws_cdk import (
    Duration,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager,
    aws_dynamodb as dynamodb,
    aws_scheduler as scheduler,
)
from constructs import Construct


class Fetcher(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        ddb_table: dynamodb.Table,
        credential_secret: secretsmanager.Secret,
        common_layer: lambda_.LayerVersion,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # Create a function to fetch sessions from the Re:Invent portal
        function = lambda_.Function(
            scope=self,
            id="FetcherFunction",
            code=lambda_.Code.from_asset("resources/functions/fetcher"),
            handler="src.index.handler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            architecture=lambda_.Architecture.X86_64,
            layers=[common_layer],
            environment={
                "DDB_TABLE_NAME": ddb_table.table_name,
                "POWERTOOLS_SERVICE_NAME": "reinvent2023_session_fetcher",
                "LOG_LEVEL": "INFO",
                "CREDENTIAL_SECRET_NAME": credential_secret.secret_name,
            },
            memory_size=1024,
            timeout=Duration.seconds(300),
        )

        # Give it the correct permissions
        credential_secret.grant_read(function)
        ddb_table.grant_read_write_data(function)

        # Create a schedule to invoke the function every minute
        scheduler_role = iam.Role(
            scope=self,
            id="FetcherSchedulerRole",
            assumed_by=iam.ServicePrincipal("scheduler.amazonaws.com"),
            inline_policies={
                "invoke_lambda": iam.PolicyDocument.from_json(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Action": ["lambda:InvokeFunction"],
                                "Effect": "Allow",
                                "Resource": function.function_arn,
                            }
                        ],
                    }
                )
            },
        )

        self.schedule = scheduler.CfnSchedule(
            scope=self,
            id="FetcherSchedule",
            schedule_expression="rate(5 minute)",
            target=scheduler.CfnSchedule.TargetProperty(
                arn=function.function_arn, role_arn=scheduler_role.role_arn
            ),
            flexible_time_window=scheduler.CfnSchedule.FlexibleTimeWindowProperty(
                mode="OFF"
            ),
        )
