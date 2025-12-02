#!/usr/bin/env python3
"""
Secure S3 Bucket with unique name - US-EAST-1
"""

from troposphere import Template, Ref, Output, Sub, Parameter
from troposphere.s3 import Bucket, PublicAccessBlockConfiguration, ServerSideEncryptionRule, ServerSideEncryptionByDefault, VersioningConfiguration, BucketEncryption
import time

# Initialize template
template = Template()
template.set_description("Secure S3 Bucket with unique name - us-east-1")

# Parameters
template.add_parameter(Parameter(
    "BucketName",
    Type="String",
    Default=f"polystudent-s3-{int(time.time())}",  # Nom unique basé sur le timestamp
    Description="Unique S3 bucket name"
))

template.add_parameter(Parameter(
    "KMSKeyARN",
    Type="String",
    Default="arn:aws:kms:us-east-1:983201656846:key/alias/aws/s3",
    Description="KMS Key ARN for encryption"
))

# Secure S3 Bucket
s3_bucket = template.add_resource(
    Bucket(
        "S3Bucket",
        DeletionPolicy="Retain",
        BucketName=Ref("BucketName"),
        AccessControl="Private",
        PublicAccessBlockConfiguration=PublicAccessBlockConfiguration(
            BlockPublicAcls=True,
            BlockPublicPolicy=True,
            IgnorePublicAcls=True,
            RestrictPublicBuckets=True
        ),
        BucketEncryption=BucketEncryption(
            ServerSideEncryptionConfiguration=[
                ServerSideEncryptionRule(
                    ServerSideEncryptionByDefault=ServerSideEncryptionByDefault(
                        SSEAlgorithm="aws:kms",
                        KMSMasterKeyID=Ref("KMSKeyARN")
                    )
                )
            ]
        ),
        VersioningConfiguration=VersioningConfiguration(
            Status="Enabled"
        )
    )
)

# Outputs
template.add_output(
    Output(
        "S3BucketName",
        Description="Secure S3 Bucket Name",
        Value=Ref(s3_bucket)
    )
)

template.add_output(
    Output(
        "S3BucketARN",
        Description="Secure S3 Bucket ARN",
        Value=Sub("arn:aws:s3:::${S3Bucket}")
    )
)

# Generate CloudFormation template
if __name__ == "__main__":
    with open("s3_bucket_unique_template.yaml", "w") as f:
        f.write(template.to_yaml())
    print("Secure S3 Bucket template with unique name generated: s3_bucket_unique_template.yaml")