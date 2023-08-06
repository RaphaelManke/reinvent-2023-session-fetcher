from aws_cdk import (
    Duration,
    aws_lambda as lambda_,
    aws_secretsmanager as secretsmanager,
    aws_dynamodb as dynamodb,
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

        self.function = lambda_.Function(
            scope=self,
            id="FetcherFunction",
            code=lambda_.Code.from_asset("resources/functions/fetcher"),
            handler="index.handler",
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
            timeout=Duration.seconds(30),
        )

        credential_secret.grant_read(self.function)
        ddb_table.grant_read_write_data(self.function)
