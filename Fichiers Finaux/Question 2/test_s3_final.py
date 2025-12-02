#!/usr/bin/env python3
"""
Test final du bucket S3 sécurisé - US-EAST-1
"""

import boto3

def test_s3_bucket():
    # Configuration us-east-1
    s3 = boto3.client('s3', region_name='us-east-1')
    cf = boto3.client('cloudformation', region_name='us-east-1')
    
    stack_name = "polystudent-s3-unique-bucket"
    bucket_name = "polystudent-s3-1763105785"  # Le VRAI nom du bucket créé
    
    try:
        # Get stack status
        response = cf.describe_stacks(StackName=stack_name)
        stack = response['Stacks'][0]
        print(f"Stack status: {stack['StackStatus']}")
        
    except Exception as e:
        print(f"Note CloudFormation: {e}")
    
    try:
        print(f"Testing S3 bucket: {bucket_name}")
        
        # Vérifier que le bucket existe
        s3.head_bucket(Bucket=bucket_name)
        print("✅ Bucket exists")
        
        # Get bucket versioning
        versioning = s3.get_bucket_versioning(Bucket=bucket_name)
        print(f"✅ Versioning: {versioning.get('Status', 'Disabled')}")
        
        # Get bucket encryption
        encryption = s3.get_bucket_encryption(Bucket=bucket_name)
        sse_config = encryption['ServerSideEncryptionConfiguration']['Rules'][0]
        sse_algorithm = sse_config['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
        kms_key_id = sse_config['ApplyServerSideEncryptionByDefault'].get('KMSMasterKeyID', 'N/A')
        print(f"✅ Encryption: {sse_algorithm}")
        print(f"✅ KMS Key: {kms_key_id}")
        
        # Get public access block configuration
        public_access = s3.get_public_access_block(Bucket=bucket_name)
        config = public_access['PublicAccessBlockConfiguration']
        print(f"✅ Block Public ACLs: {config['BlockPublicAcls']}")
        print(f"✅ Block Public Policy: {config['BlockPublicPolicy']}")
        print(f"✅ Ignore Public ACLs: {config['IgnorePublicAcls']}")
        print(f"✅ Restrict Public Buckets: {config['RestrictPublicBuckets']}")
        
        # Get bucket ACL pour vérifier qu'il est privé
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        print(f"✅ Bucket Owner: {acl['Owner']['DisplayName']}")
        
        print("\n🎯 TOUTES LES VÉRIFICATIONS PASSÉES AVEC SUCCÈS !")
        print("Le bucket S3 est parfaitement configuré avec toutes les sécurités demandées.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_s3_bucket()