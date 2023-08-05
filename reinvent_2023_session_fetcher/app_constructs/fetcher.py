from aws_cdk import (
    Duration,
    aws_lambda as lambda_,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct


class Fetcher(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        credential_secret: secretsmanager.Secret,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        layer = lambda_.LayerVersion(
            scope=self,
            id="FetcherFunctionLayer",
            code=lambda_.Code.from_asset("resources/layers/fetcher/python.zip"),
        )

        function = lambda_.Function(
            scope=self,
            id="FetcherFunction",
            code=lambda_.Code.from_asset("resources/functions/fetcher"),
            handler="index.handler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            architecture=lambda_.Architecture.X86_64,
            layers=[layer],
            environment={
                "POWERTOOLS_SERVICE_NAME": "reinvent2023_session_fetcher",
                "LOG_LEVEL": "INFO",
                "CREDENTIAL_SECRET_NAME": credential_secret.secret_name,
            },
            memory_size=1024,
            timeout=Duration.seconds(30),
        )

        credential_secret.grant_read(function)
