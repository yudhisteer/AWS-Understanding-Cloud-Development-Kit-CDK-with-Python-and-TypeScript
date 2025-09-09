from aws_cdk import (
    Stack,
    aws_lambda,
    aws_sns,
    aws_sns_subscriptions,
    aws_cloudwatch,
    Duration,
    aws_cloudwatch_actions,
)
from constructs import Construct

class PyCwMetricsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda Function Configuration
        # Creates a Lambda function that will receive SNS messages from CloudWatch alarms
        # and forward them to a Slack webhook for team notifications
        lambda_function = aws_lambda.Function(
            scope=self,
            id="WebHookLambdaFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_10,  # Python 3.10 runtime environment
            code=aws_lambda.Code.from_asset("services"),  # Load code from local 'services' directory
            handler="hook.handler",  # Entry point: handler function in hook.py file
        )

        # SNS Topic Configuration
        # Creates an SNS topic that serves as the communication bridge between
        # CloudWatch alarms and the Lambda function for decoupled messaging
        topic = aws_sns.Topic(
            scope=self,
            id="WebHookTopic",
            display_name="WebHookTopic",  # Human-readable name shown in AWS console
            topic_name="WebHookTopic",    # Actual topic name used for ARN generation
        )

        # Lambda-SNS Integration
        # Subscribes the Lambda function to the SNS topic so it automatically
        # receives and processes all messages published to this topic
        topic.add_subscription(aws_sns_subscriptions.LambdaSubscription(fn=lambda_function))

        # CloudWatch Alarm Configuration
        # Monitors a custom metric and triggers notifications when thresholds are breached
        # This alarm watches for unusual activity in the 'MyCustomMetric' metric
        alarm = aws_cloudwatch.Alarm(
            scope=self,
            id="WebHookAlarm",
            metric=aws_cloudwatch.Metric(
                namespace="MyCustomNamespace",  
                metric_name="MyCustomMetric",  
                statistic="Sum",                # Aggregation method: sum all values in period
                period=Duration.minutes(1),    # Evaluation window: check every 1 minute
            ),
            evaluation_periods=1,  # Number of consecutive periods before triggering (1 = immediate)
            threshold=100,         # Alert threshold: trigger when sum exceeds 100
        )

        # Alarm Action Configuration
        # Sets up SNS notifications for both alarm state changes (ALARM and OK states)
        # This ensures the team is notified when issues arise AND when they're resolved
        topic_action = aws_cloudwatch_actions.SnsAction(topic=topic)
        alarm.add_alarm_action(topic_action)  # Send notification when metric breaches threshold
        alarm.add_ok_action(topic_action)     # Send notification when metric returns to normal


        """
        Second Alarm for API
        """
        # API Gateway CloudWatch Alarm Configuration
        # Monitors 4XX client errors from API Gateway and triggers notifications
        # when error rates exceed acceptable thresholds for proactive issue resolution
        api_alarm = aws_cloudwatch.Alarm(
            self,
            "Py-Api4xxAlarm",  # Unique identifier for the API Gateway 4XX error alarm
            metric=aws_cloudwatch.Metric(
                metric_name="4XXError",         # AWS API Gateway built-in metric for client errors
                namespace="AWS/ApiGateway",     # AWS-managed namespace for API Gateway metrics
                statistic="Sum",               
                dimensions_map={
                    "ApiName": "PyRestApi"      # Filter metric to specific API Gateway instance
                }
            ),
            evaluation_periods=1,  # Trigger immediately on first threshold breach
            threshold=1,           # Alert on any 4XX errors (zero tolerance for client errors)
        )

        # API Gateway Alarm Action Configuration
        api_alarm.add_alarm_action(topic_action)  # Notify when 4XX errors detected
        api_alarm.add_ok_action(topic_action)     # Notify when error rate returns to normal