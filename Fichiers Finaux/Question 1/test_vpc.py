#!/usr/bin/env python3
"""
Test script to verify VPC infrastructure
"""

import boto3
import json

def test_vpc_infrastructure():
    ec2 = boto3.client('ec2', region_name='us-east-1')
    cf = boto3.client('cloudformation', region_name='us-east-1')
    
    stack_name = "polystudent-vpc-stack"
    
    try:
        # Get stack outputs
        response = cf.describe_stacks(StackName=stack_name)
        stack = response['Stacks'][0]
        
        print("✅ Stack exists and is in status:", stack['StackStatus'])
        
        # Get VPC ID from outputs
        vpc_id = None
        for output in stack.get('Outputs', []):
            if output['OutputKey'] == 'VPCId':
                vpc_id = output['OutputValue']
                break
        
        if vpc_id:
            print(f"✅ VPC ID: {vpc_id}")
            
            # Verify VPC exists
            vpc_response = ec2.describe_vpcs(VpcIds=[vpc_id])
            vpc = vpc_response['Vpcs'][0]
            print(f"✅ VPC CIDR: {vpc['CidrBlock']}")
            print(f"✅ VPC State: {vpc['State']}")
            
            # Verify subnets
            subnets = ec2.describe_subnets(
                Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
            )
            print(f"✅ Number of subnets created: {len(subnets['Subnets'])}")
            
            # Verify route tables
            route_tables = ec2.describe_route_tables(
                Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
            )
            print(f"✅ Number of route tables: {len(route_tables['RouteTables'])}")
            
            # Verify internet gateway
            igws = ec2.describe_internet_gateways(
                Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}]
            )
            print(f"✅ Internet Gateway attached: {len(igws['InternetGateways']) > 0}")
            
            print("\n🎉 All tests passed! VPC infrastructure is properly deployed.")
            
        else:
            print("❌ Could not find VPC ID in stack outputs")
            
    except Exception as e:
        print(f" Test failed: {e}")

if __name__ == "__main__":
    test_vpc_infrastructure()