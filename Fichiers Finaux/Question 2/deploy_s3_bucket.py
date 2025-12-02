#!/usr/bin/env python3
"""
Deploy Secure S3 Bucket using AWS CloudFormation - US-EAST-1
"""

import boto3
import os

def deploy_s3_bucket():
    # Forcer la région us-east-1
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    
    # Initialize CloudFormation client avec région explicite
    cf_client = boto3.client('cloudformation', region_name='us-east-1')
    
    stack_name = "polystudent-s3-secure-bucket"
    
    try:
        # Read template
        with open('s3_bucket_template.yaml', 'r') as f:
            template_body = f.read()
    except FileNotFoundError:
        print("Error: s3_bucket_template.yaml not found.")
        return

    try:
        # Create stack
        response = cf_client.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=[
                {
                    'ParameterKey': 'BucketName',
                    'ParameterValue': 'polystudents3-secure-983201656846'
                },
                {
                    'ParameterKey': 'KMSKeyARN', 
                    'ParameterValue': 'arn:aws:kms:us-east-1:983201656846:key/alias/aws/s3'
                }
            ],
            Capabilities=['CAPABILITY_IAM'],
            Tags=[
                {'Key': 'Project', 'Value': 'PolyStudent'},
                {'Key': 'Environment', 'Value': 'Production'}
            ]
        )
        
        print(f"Stack creation in us-east-1: {response['StackId']}")
        print("Waiting for stack creation to complete...")
        
        # Wait for completion
        waiter = cf_client.get_waiter('stack_create_complete')
        waiter.wait(StackName=stack_name)
        print("Stack creation completed successfully in us-east-1!")
        
        # Get outputs
        stacks = cf_client.describe_stacks(StackName=stack_name)
        stack = stacks['Stacks'][0]
        
        print("Stack Outputs:")
        for output in stack.get('Outputs', []):
            print(f"  {output['OutputKey']}: {output['OutputValue']}")
        
    except cf_client.exceptions.AlreadyExistsException:
        print("Stack already exists in us-east-1.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    deploy_s3_bucket()