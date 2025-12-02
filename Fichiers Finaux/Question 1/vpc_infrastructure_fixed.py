#!/usr/bin/env python3
"""
VPC Infrastructure - Fixed Version
"""

from troposphere import Template, Ref, Output, Sub, Parameter, Export
from troposphere.ec2 import (
    VPC, Subnet, RouteTable, Route, 
    SubnetRouteTableAssociation, InternetGateway,
    VPCGatewayAttachment, SecurityGroup
)

template = Template()
template.set_description("VPC with Public and Private Subnets")

# Parameters
env_name_param = Parameter(
    "EnvironmentName",
    Type="String",
    Default="polystudent-vpc"
)
template.add_parameter(env_name_param)

# VPC
vpc = VPC(
    "VPC",
    CidrBlock="10.0.0.0/16",
    EnableDnsHostnames=True,
    EnableDnsSupport=True,
    Tags=[{"Key": "Name", "Value": Ref("EnvironmentName")}]
)
template.add_resource(vpc)

# Internet Gateway
igw = InternetGateway(
    "InternetGateway",
    Tags=[{"Key": "Name", "Value": Sub("${EnvironmentName}-igw")}]
)
template.add_resource(igw)

# Attach IGW
igw_attach = VPCGatewayAttachment(
    "IGWAttachment",
    VpcId=Ref(vpc),
    InternetGatewayId=Ref(igw)
)
template.add_resource(igw_attach)

# Public Subnet 1
public_subnet1 = Subnet(
    "PublicSubnet1",
    VpcId=Ref(vpc),
    CidrBlock="10.0.1.0/24",
    AvailabilityZone=Sub("${AWS::Region}a"),
    MapPublicIpOnLaunch=True,
    Tags=[{"Key": "Name", "Value": Sub("${EnvironmentName}-public-1")}]
)
template.add_resource(public_subnet1)

# Public Route Table
public_rt = RouteTable(
    "PublicRouteTable",
    VpcId=Ref(vpc),
    Tags=[{"Key": "Name", "Value": Sub("${EnvironmentName}-public-rt")}]
)
template.add_resource(public_rt)

# Internet Route
public_route = Route(
    "PublicRoute",
    RouteTableId=Ref(public_rt),
    DestinationCidrBlock="0.0.0.0/0",
    GatewayId=Ref(igw)
)
template.add_resource(public_route)

# Associate Public Subnet with Route Table
template.add_resource(SubnetRouteTableAssociation(
    "PublicSubnet1Association",
    SubnetId=Ref(public_subnet1),
    RouteTableId=Ref(public_rt)
))

# Security Group
web_sg = SecurityGroup(
    "WebSecurityGroup",
    GroupDescription="Web Security Group",
    VpcId=Ref(vpc),
    SecurityGroupIngress=[
        {
            "IpProtocol": "tcp",
            "FromPort": "80",
            "ToPort": "80", 
            "CidrIp": "0.0.0.0/0"
        },
        {
            "IpProtocol": "tcp",
            "FromPort": "22",
            "ToPort": "22",
            "CidrIp": "0.0.0.0/0"
        }
    ],
    Tags=[{"Key": "Name", "Value": Sub("${EnvironmentName}-web-sg")}]
)
template.add_resource(web_sg)

# Outputs
template.add_output(Output(
    "VPCId",
    Description="VPC ID",
    Value=Ref(vpc),
    Export=Export(Sub("${EnvironmentName}-vpc-id"))
))

template.add_output(Output(
    "PublicSubnet1Id",
    Description="Public Subnet 1 ID",
    Value=Ref(public_subnet1),
    Export=Export(Sub("${EnvironmentName}-public-subnet-1"))
))

template.add_output(Output(
    "SecurityGroupId", 
    Description="Web Security Group ID",
    Value=Ref(web_sg),
    Export=Export(Sub("${EnvironmentName}-web-sg-id"))
))

if __name__ == "__main__":
    with open("vpc_fixed_template.yaml", "w") as f:
        f.write(template.to_yaml())
    print("Fixed template generated: vpc_fixed_template.yaml")