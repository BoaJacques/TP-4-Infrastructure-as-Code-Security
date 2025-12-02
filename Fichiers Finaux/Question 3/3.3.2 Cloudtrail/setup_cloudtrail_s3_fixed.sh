#!/bin/bash

# Exercice 3.3.2 - Activation de CloudTrail pour le bucket S3 (Version corrigée)

set -e

echo "=== CONFIGURATION CLOUDTRAIL POUR S3 - EXERCICE 3.3.2 ==="

# Variables avec noms uniques
TIMESTAMP=$(date +%s)
S3_BUCKET="polystudens3"  # On tente avec le nom original d'abord
CLOUDTRAIL_NAME="S3ObjectActivityTrail-$TIMESTAMP"
S3_LOGS_BUCKET="polystudent-ct-logs-$TIMESTAMP"
REGION="us-east-1"

echo "Utilisation de noms uniques:"
echo "Piste CloudTrail: $CLOUDTRAIL_NAME"
echo "Bucket logs: $S3_LOGS_BUCKET"

# 1. Créer un bucket S3 pour stocker les logs CloudTrail
echo "1. Création du bucket pour les logs CloudTrail..."
aws s3 mb s3://$S3_LOGS_BUCKET --region $REGION

# Configurer la politique de bucket pour CloudTrail
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

cat > cloudtrail-bucket-policy.json << POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailAclCheck",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::$S3_LOGS_BUCKET"
        },
        {
            "Sid": "AWSCloudTrailWrite",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::$S3_LOGS_BUCKET/AWSLogs/$ACCOUNT_ID/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        }
    ]
}
POLICY

aws s3api put-bucket-policy \
    --bucket $S3_LOGS_BUCKET \
    --policy file://cloudtrail-bucket-policy.json

# 2. Vérifier si le bucket S3 à monitorer existe, sinon le créer
echo "2. Vérification du bucket S3 à monitorer..."
if ! aws s3 ls s3://$S3_BUCKET &>/dev/null; then
    echo "Création du bucket $S3_BUCKET..."
    S3_BUCKET="polystudent-source-$TIMESTAMP"
    aws s3 mb s3://$S3_BUCKET --region $REGION
    aws s3api put-bucket-versioning \
        --bucket $S3_BUCKET \
        --versioning-configuration Status=Enabled
    echo "Nouveau bucket créé: $S3_BUCKET"
else
    echo "Bucket existant utilisé: $S3_BUCKET"
fi

# 3. Créer la piste CloudTrail
echo "3. Création de la piste CloudTrail..."

aws cloudtrail create-trail \
    --name $CLOUDTRAIL_NAME \
    --s3-bucket-name $S3_LOGS_BUCKET \
    --is-multi-region-trail \
    --enable-log-file-validation

echo "Piste CloudTrail créée: $CLOUDTRAIL_NAME"

# 4. Configurer les événements de gestion de données S3
echo "4. Configuration des événements S3..."

cat > event-selectors.json << EVENTS
[
    {
        "ReadWriteType": "All",
        "IncludeManagementEvents": true,
        "DataResources": [
            {
                "Type": "AWS::S3::Object",
                "Values": [
                    "arn:aws:s3:::$S3_BUCKET/"
                ]
            }
        ]
    }
]
EVENTS

aws cloudtrail put-event-selectors \
    --trail-name $CLOUDTRAIL_NAME \
    --event-selectors file://event-selectors.json

# 5. Activer la journalisation
echo "5. Activation de la journalisation CloudTrail..."
aws cloudtrail start-logging --name $CLOUDTRAIL_NAME

# 6. Tester la configuration
echo "6. Test de la configuration CloudTrail..."

# Créer un fichier de test
echo "Test file for CloudTrail monitoring - Object modification" > cloudtrail-test.txt

# Effectuer des opérations sur le bucket S3
echo "Upload d'un fichier de test..."
aws s3 cp cloudtrail-test.txt s3://$S3_BUCKET/cloudtrail-test-upload.txt

echo "Modification du fichier..."
echo "Modified content - $(date)" > cloudtrail-test-modified.txt
aws s3 cp cloudtrail-test-modified.txt s3://$S3_BUCKET/cloudtrail-test-upload.txt

echo "Suppression du fichier..."
aws s3 rm s3://$S3_BUCKET/cloudtrail-test-upload.txt

echo "Attente de la génération des logs (30 secondes)..."
sleep 30

# 7. Vérifier les logs CloudTrail
echo "7. Vérification des logs CloudTrail..."

echo "Statut de la piste:"
aws cloudtrail get-trail-status --name $CLOUDTRAIL_NAME

echo "Fichiers de logs CloudTrail créés:"
aws s3 ls s3://$S3_LOGS_BUCKET/AWSLogs/$ACCOUNT_ID/CloudTrail/ --recursive | head -5

# 8. Vérifier les événements récents
echo "Événements CloudTrail récents pour S3:"
aws cloudtrail lookup-events --max-results 3 --output table

# Nettoyer
rm -f cloudtrail-bucket-policy.json event-selectors.json cloudtrail-test.txt cloudtrail-test-modified.txt

echo "=== CONFIGURATION CLOUDTRAIL TERMINEE ==="
echo "Piste CloudTrail: $CLOUDTRAIL_NAME"
echo "Bucket monitoré: $S3_BUCKET"
echo "Bucket de logs: $S3_LOGS_BUCKET"
echo "Région: $REGION"

# Informations de vérification
echo ""
echo "=== INFORMATIONS DE VERIFICATION ==="
aws cloudtrail describe-trails --trail-name-list $CLOUDTRAIL_NAME
