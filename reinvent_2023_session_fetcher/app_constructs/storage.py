from aws_cdk import (
    RemovalPolicy,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct


class Storage(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create a CDK DynamoDB Table
        self.table = dynamodb.Table(
            scope=self,
            id="ReInventSessionTable",
            table_name="ReInventSessionTable",
            partition_key=dynamodb.Attribute(
                name="PK", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(name="SK", type=dynamodb.AttributeType.STRING),
            stream=dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Secret for the Reinvent website user credentials
        self.credentials_secret = secretsmanager.Secret(
            scope=self,
            id="ReInventCredentialsSecret",
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.common_layer = lambda_.LayerVersion(
            scope=self,
            id="CommonFunctionLayer",
            code=lambda_.Code.from_asset("resources/layers/common/python.zip"),
            removal_policy=RemovalPolicy.DESTROY,
        )
