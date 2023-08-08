from aws_cdk import (
    Duration,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class RestApi(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        ddb_table: dynamodb.Table,
        common_layer: lambda_.LayerVersion,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # Create the RestAPI
        rest_api = apigateway.RestApi(
            scope=self,
            id="ReInvent2023SessionsApi",
            rest_api_name="ReInvent2023SessionsApi",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS
            ),
            endpoint_types=[apigateway.EndpointType.REGIONAL],
            deploy_options=apigateway.StageOptions(
                caching_enabled=True,
                cache_ttl=Duration.seconds(300),
            ),
        )

        # Create a Lambda function to handle the /mutations resource
        handler_lambda = lambda_.Function(
            scope=self,
            id="ReInvent2023SessionsApiFunction",
            code=lambda_.Code.from_asset("resources/functions/api"),
            handler="index.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            architecture=lambda_.Architecture.X86_64,
            layers=[common_layer],
            environment={
                "DDB_TABLE_NAME": ddb_table.table_name,
                "POWERTOOLS_SERVICE_NAME": "reinvent2023_session_api_get_mutations",
                "LOG_LEVEL": "INFO",
            },
            memory_size=1024,
            timeout=Duration.seconds(30),
        )
        ddb_table.grant_read_data(handler_lambda)

        # Create the /mutations resource
        mutations = rest_api.root.add_resource("mutations")
        # Create the /sessions resource
        sessions = rest_api.root.add_resource("sessions")
        # Create the /sessions/{session_id} resource
        session = sessions.add_resource("{session_id}")
        # Create the /sessions/{session_id}/history resource
        session_history = session.add_resource("history")

        mutations.add_method(
            http_method="GET",
            integration=apigateway.LambdaIntegration(
                handler=handler_lambda, allow_test_invoke=False
            ),
        )

        sessions.add_method(
            http_method="GET",
            integration=apigateway.LambdaIntegration(
                handler=handler_lambda, allow_test_invoke=False
            ),
        )

        session.add_method(
            http_method="GET",
            integration=apigateway.LambdaIntegration(
                handler=handler_lambda, allow_test_invoke=False
            ),
        )

        session_history.add_method(
            http_method="GET",
            integration=apigateway.LambdaIntegration(
                handler=handler_lambda, allow_test_invoke=False
            ),
        )
