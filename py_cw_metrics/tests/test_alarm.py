import boto3

def put_test_metric(value: float):
    client = boto3.client('cloudwatch')
    client.put_metric_data(
        Namespace='MyCustomNamespace',
        MetricData=[
            {
                'MetricName': 'MyCustomMetric',
                'Value': value,
                'Unit': 'None'
            }
        ]
    )
    print(f"Put metric data: {value} to MyCustomMetric in MyCustomNamespace")

if __name__ == '__main__':
    put_test_metric(value=1000.0)
