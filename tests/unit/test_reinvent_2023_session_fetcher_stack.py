import aws_cdk as core
import aws_cdk.assertions as assertions

from reinvent_2023_session_fetcher.reinvent_2023_session_fetcher_stack import (
    Reinvent2023SessionFetcherStack,
)


# example tests. To run these tests, uncomment this file along with the example
# resource in reinvent_2023_session_fetcher/reinvent_2023_session_fetcher_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Reinvent2023SessionFetcherStack(app, "reinvent-2023-session-fetcher")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
