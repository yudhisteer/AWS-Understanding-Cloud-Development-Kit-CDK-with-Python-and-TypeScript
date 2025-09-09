# AWS-Understanding-Cloud-Development-Kit-CDK-with-Python-and-TypeScript


<img width="1888" height="676" alt="image" src="https://github.com/user-attachments/assets/fb452c02-9d9b-4f16-8f33-995905cb49cc" />

<img width="1892" height="677" alt="image" src="https://github.com/user-attachments/assets/ee74739e-0477-4bbc-9c53-87fb4bcdd248" />

<img width="1896" height="848" alt="image" src="https://github.com/user-attachments/assets/8528d948-5cea-47be-a9a6-49f7dafad85a" />

<img width="1885" height="673" alt="image" src="https://github.com/user-attachments/assets/c677f4a2-c494-4d0f-8b7b-c09afbc239e5" />

<img width="1888" height="786" alt="image" src="https://github.com/user-attachments/assets/2b3518d3-6a4b-4746-9772-207df84c566a" />

<img width="1890" height="680" alt="image" src="https://github.com/user-attachments/assets/5e9e6d35-0293-40a0-a579-cb0b4aa7ce32" />

<img width="1881" height="776" alt="image" src="https://github.com/user-attachments/assets/e78f01ee-fe51-4021-94d5-8b2ed94daff9" />


<img width="1889" height="468" alt="image" src="https://github.com/user-attachments/assets/de4c516f-3d13-4982-855a-346fd3ea0307" />


<img width="1881" height="359" alt="image" src="https://github.com/user-attachments/assets/c8ca73ac-a1e0-4edd-b012-e11cf06261d6" />



## Some useful commands: 

cdk bootstrap <aws-account-id>/region: bootstrap the AWS account

cdk synth: create cloudformation template

cdk deploy: deploy the stack to the AWS account

cdk destroy: destroy the stack from the AWS account

cdk diff: show the differences between the current stack and the stack in the AWS account

cdk docs: open the CDK documentation

cdk list: list all the stacks in the AWS account

# Example command to put metric data to CloudWatch
aws cloudwatch put-metric-data --namespace MyCustomNamespace --metric-name MyCustomMetric --value 1 --unit Count --dimensions Key=Value --region us-east-1

# Example command to describe the alarms
aws cloudwatch describe-alarms --alarm-names "test alarm"


```yaml
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 13
Connection: close
Date: Mon, 08 Sep 2025 18:26:36 GMT
X-Amzn-Trace-Id: Root=1-68bf1fdc-1848d6c62fd1f5545e60dd99;Parent=25d0056adb1c0ad2;Sampled=0;Lineage=1:b5d3d54f:0
x-amzn-RequestId: 1b97b59c-3bf9-4d30-b6c9-1b71805dcd09
x-amz-apigw-id: QmHqjEtEoAMEfsA=
X-Cache: Miss from cloudfront
Via: 1.1 d6a002c70d55f415107618b0750d493c.cloudfront.net (CloudFront)
X-Amz-Cf-Pop: SEA19-C2
X-Amz-Cf-Id: KIDa1rMDQhV4Z15EBLYMtlX6h5ZDBPPw03YH6cnv46mLA0ENngso8w==

Hello, World!
```



## References:
- https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Fn.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html
- https://aws.amazon.com/blogs/compute/best-practices-for-organizing-larger-serverless-applications/
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html
