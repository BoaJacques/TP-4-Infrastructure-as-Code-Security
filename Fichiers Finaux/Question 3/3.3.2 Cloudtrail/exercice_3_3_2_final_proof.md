# PREUVE D'ACHÈVEMENT - Exercice 3.3.2
## Activation de CloudTrail pour monitorer les activités S3

### TÂCHES ACCOMPLIES :

1. **Bucket dédié pour logs CloudTrail créé**
   - Nom: polystudent-ct-logs-1763342392
   - Politique de bucket configurée pour autoriser CloudTrail
   - Accès sécurisé avec condition s3:x-amz-acl

2. **Piste CloudTrail multi-région configurée**
   - Nom: S3ObjectActivityTrail-1763342392
   - ARN: arn:aws:cloudtrail:us-east-1:983201656846:trail/S3ObjectActivityTrail-1763342392
   - Validation des fichiers de logs activée
   - Journalisation activée (IsLogging: true)

3. **Sélecteurs d'événements S3 spécifiques**
   - Monitoring de toutes les opérations (ReadWriteType: All)
   - Bucket cible: polystudent-source-1763342392
   - Ressource: arn:aws:s3:::polystudent-source-1763342392/
   - Événements de gestion inclus

4. **Test complet des fonctionnalités**
   - Upload d'objet: cloudtrail-test-upload.txt
   - Modification d'objet: remplacement du fichier
   - Suppression d'objet: suppression réussie
   - Logs CloudTrail générés avec succès

### CONFIGURATION DÉPLOYÉE :

**Infrastructure CloudTrail**:
- Piste: S3ObjectActivityTrail-1763342392
- Type: Multi-région
- Log Validation: Enabled
- Statut: Logging activé depuis 2025-11-17T01:20:05Z

**Monitoring S3**:
- Bucket cible: polystudent-source-1763342392
- Opérations: PutObject, GetObject, DeleteObject, etc.
- Ressource: arn:aws:s3:::polystudent-source-1763342392/

**Stockage des logs**:
- Bucket: polystudent-ct-logs-1763342392
- Compte: 983201656846
- Structure: AWSLogs/983201656846/CloudTrail/

### ÉVÉNEMENTS MONITORÉS ET TESTÉS :

- Création d'objets: Upload de cloudtrail-test-upload.txt
- Modification d'objets: Remplacement avec cloudtrail-test-modified.txt
- Suppression d'objets: Delete de cloudtrail-test-upload.txt
- Accès aux objets: Toutes les opérations de lecture/écriture
- Activités de gestion du bucket

### VÉRIFICATIONS EFFECTUÉES :

Statut CloudTrail - CONFIRMÉ
aws cloudtrail get-trail-status --name S3ObjectActivityTrail-1763342392
Résultat: "IsLogging": true

Logs générés - CONFIRMÉ
aws s3 ls s3://polystudent-ct-logs-1763342392/AWSLogs/983201656846/CloudTrail/
Structure créée avec succès

Configuration de la piste - CONFIRMÉ
aws cloudtrail describe-trails --trail-name-list S3ObjectActivityTrail-1763342392
Piste active et configurée

### RÉSULTAT :
CloudTrail configuré avec succès pour capturer et logger toutes les activités de modification, suppression et accès aux objets dans le bucket S3 polystudent-source-1763342392. Les logs sont stockés de manière sécurisée dans polystudent-ct-logs-1763342392 et peuvent être utilisés pour l'audit et la conformité.

Toutes les opérations de test (upload, modification, suppression) ont été exécutées avec succès et sont maintenant monitorées par CloudTrail.

Méthode: Script Bash avec AWS CLI
Région: us-east-1
Timestamp: 1763342392
Date d'achèvement: 2025-11-16 20:20
Étudiant: J@cques Bo@
Cours: Infonuagique - TP3
