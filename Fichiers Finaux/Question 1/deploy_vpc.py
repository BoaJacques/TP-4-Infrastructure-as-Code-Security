#!/usr/bin/env python3
"""
Deploy VPC infrastructure using AWS CloudFormation
"""

import boto3
import time
import json

def deploy_vpc_stack():
    # Initialize CloudFormation client
    cf_client = boto3.client('cloudformation', region_name='us-east-1')
    
    stack_name = "polystudent-vpc-stack"
    
    # Read template
    with open('vpc_template.yaml', 'r') as f:
        template_body = f.read()
    
    try:
        # Create or update stack
        response = cf_client.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=[
                {
                    'ParameterKey': 'EnvironmentName',
                    'ParameterValue': 'polystudent-vpc'
                }
            ],
            Capabilities=['CAPABILITY_IAM'],
            Tags=[
                {
                    'Key': 'Project',
                    'Value': 'PolyStudent'
                }
            ]
        )
        
        print(f"Stack creation initiated: {response['StackId']}")
        
        # Wait for completion
        waiter = cf_client.get_waiter('stack_create_complete')
        waiter.wait(StackName=stack_name)
        
        print(" Stack creation completed successfully!")
        
        # Get outputs
        stacks = cf_client.describe_stacks(StackName=stack_name)
        stack = stacks['Stacks'][0]
        
        print("\n Stack Outputs:")
        for output in stack.get('Outputs', []):
            print(f"  {output['OutputKey']}: {output['OutputValue']}")
            
    except cf_client.exceptions.AlreadyExistsException:
        print("Stack already exists. Updating...")
        
        response = cf_client.update_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=[
                {
                    'ParameterKey': 'EnvironmentName', 
                    'ParameterValue': 'polystudent-vpc'
                }
            ],
            Capabilities=['CAPABILITY_IAM']
        )
        print(f"Stack update initiated: {response['StackId']}")

if __name__ == "__main__":
    deploy_vpc_stack()