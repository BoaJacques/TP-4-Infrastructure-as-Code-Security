#!/usr/bin/env python3
"""
Deploy S3 Bucket with replication - US-EAST-1
Updated for Exercise 3.3
"""

import boto3
import time

def deploy_s3_replication():
    # Configuration us-east-1
    cf_client = boto3.client('cloudformation', region_name='us-east-1')
    
    stack_name = "polystudent-s3-replication"
    
    try:
        # Read template
        with open('s3_bucket_replication_template.yaml', 'r') as f:
            template_body = f.read()
    except FileNotFoundError:
        print("Error: Template file not found.")
        return

    try:
        # Create stack with replication
        response = cf_client.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=[
                {
                    'ParameterKey': 'BucketName',
                    'ParameterValue': 'polystudens3'
                },
                {
                    'ParameterKey': 'DestinationBucketName',
                    'ParameterValue': 'polystudents3-back'  
                },
                {
                    'ParameterKey': 'KMSKeyARN', 
                    'ParameterValue': 'arn:aws:kms:us-east-1:983201656846:key/alias/aws/s3'
                }
            ],
            Capabilities=['CAPABILITY_IAM'],
            Tags=[
                {'Key': 'Project', 'Value': 'PolyStudent'},
                {'Key': 'Environment', 'Value': 'Production'},
                {'Key': 'Exercise', 'Value': '3.3'}
            ]
        )
        
        print(f"Stack creation: {response['StackId']}")
        print("Creating S3 buckets with replication...")
        print("Source bucket: polystudens3")
        print("Destination bucket: polystudents3-back")
        print("Waiting for stack creation...")
        
        # Wait for completion
        waiter = cf_client.get_waiter('stack_create_complete')
        waiter.wait(StackName=stack_name)
        print("Stack creation completed successfully!")
        
        # Get outputs
        stacks = cf_client.describe_stacks(StackName=stack_name)
        stack = stacks['Stacks'][0]
        
        print("Stack Outputs:")
        for output in stack.get('Outputs', []):
            print(f"  {output['OutputKey']}: {output['OutputValue']}")
        
        # Test replication
        print("\nTesting replication...")
        s3_client = boto3.client('s3', region_name='us-east-1')
        
        # Upload test file
        test_content = b"This is a test file for S3 replication - Exercise 3.3"
        s3_client.put_object(
            Bucket='polystudens3',
            Key='test-replication.txt',
            Body=test_content
        )
        print("Test file uploaded to source bucket: test-replication.txt")
        print("Replication should occur automatically within a few minutes...")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    deploy_s3_replication()