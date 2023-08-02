from aws_cdk import (
    Duration,
    aws_lambda as lambda_,
)
from constructs import Construct


class Fetcher(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        layer = lambda_.LayerVersion(
            scope=self,
            id="FetcherFunctionLayer",
            code=lambda_.Code.from_asset("resources/layers/fetcher/python.zip"),
        )

        lambda_.Function(
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
            },
            memory_size=1024,
            timeout=Duration.seconds(30),
        )
