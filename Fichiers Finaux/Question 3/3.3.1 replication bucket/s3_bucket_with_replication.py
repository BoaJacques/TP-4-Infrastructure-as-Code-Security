#!/usr/bin/env python3
"""
Generate a CloudFormation template for:
- Source bucket with replication (polystudents3 or autre via param)
- Destination bucket (polystudents3-back)
- IAM Role for S3 replication

This script writes: s3_bucket_replication_template.yaml
"""

TEMPLATE = """AWSTemplateFormatVersion: '2010-09-09'
Description: Secure S3 Bucket with replication to polystudents3-back - us-east-1

Parameters:
  BucketName:
    Type: String
    Default: polystudents3
    Description: Source S3 bucket name
  DestinationBucketName:
    Type: String
    Default: polystudents3-back
    Description: Destination S3 bucket name for replication
  KMSKeyARN:
    Type: String
    Default: arn:aws:kms:us-east-1:983201656846:alias/aws/s3
    Description: KMS Key ARN for encryption

Resources:
  S3DestinationBucket:
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    Properties:
      BucketName: !Ref DestinationBucketName
      AccessControl: Private
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: aws:kms
              KMSMasterKeyID: !Ref KMSKeyARN
      VersioningConfiguration:
        Status: Enabled

  S3ReplicationRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: s3.amazonaws.com
            Action: sts:AssumeRole
      Path: /
      Policies:
        - PolicyName: S3ReplicationPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetReplicationConfiguration
                  - s3:ListBucket
                Resource: !Sub arn:aws:s3:::${BucketName}
              - Effect: Allow
                Action:
                  - s3:GetObjectVersionForReplication
                  - s3:GetObjectVersionAcl
                  - s3:GetObjectVersionTagging
                Resource: !Sub arn:aws:s3:::${BucketName}/*
              - Effect: Allow
                Action:
                  - s3:ReplicateObject
                  - s3:ReplicateDelete
                  - s3:ReplicateTags
                Resource: !Sub arn:aws:s3:::${DestinationBucketName}/*

  S3SourceBucket:
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    Properties:
      BucketName: !Ref BucketName
      AccessControl: Private
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: aws:kms
              KMSMasterKeyID: !Ref KMSKeyARN
      VersioningConfiguration:
        Status: Enabled
      ReplicationConfiguration:
        Role: !GetAtt S3ReplicationRole.Arn
        Rules:
          - Id: FullBucketReplication
            Status: Enabled
            Prefix: ''
            DeleteMarkerReplication:
              Status: Enabled
            Destination:
              Bucket: !Sub arn:aws:s3:::${DestinationBucketName}
              StorageClass: STANDARD

Outputs:
  S3SourceBucketName:
    Description: Source S3 Bucket Name
    Value: !Ref S3SourceBucket
  S3DestinationBucketName:
    Description: Destination S3 Bucket Name
    Value: !Ref S3DestinationBucket
  ReplicationRoleARN:
    Description: S3 Replication Role ARN
    Value: !GetAtt S3ReplicationRole.Arn
"""

if __name__ == "__main__":
    with open("s3_bucket_replication_template.yaml", "w") as f:
        f.write(TEMPLATE)
    print("S3 Bucket with replication template generated: s3_bucket_replication_template.yaml")
