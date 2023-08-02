from aws_cdk import (
    aws_dynamodb as dynamodb,
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
            partition_key=dynamodb.Attribute(name="PK", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="SK", type=dynamodb.AttributeType.STRING)
        )
        
