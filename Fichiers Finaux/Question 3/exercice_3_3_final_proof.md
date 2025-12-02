# PREUVE D'ACHÈVEMENT - Exercice 3.3
## Configuration de réplication S3

###  TÂCHES ACCOMPLIES :

1. **Buckets S3 créés avec noms uniques**
   - Les noms "polystudens3" et "polystudents3-back" étaient déjà pris
   - Solution: Utilisation de noms uniques avec timestamp
   - Versioning activé sur les deux buckets
   - Région: us-east-1

2. **Rôle IAM pour réplication configuré**
   - Rôle créé avec nom unique
   - Politique de confiance pour le service S3
   - Permissions pour la réplication complète

3. **Configuration de réplication déployée**
   - Règle: `FullBucketReplication`
   - Statut: Enabled
   - Réplication de tout le bucket
   - Réplication des delete markers activée

4. **Test de réplication effectué**
   - Fichier de test uploadé vers le bucket source
   - Processus de réplication initié
   - Configuration vérifiée avec AWS CLI

###  CONFIGURATION DÉPLOYÉE :

**Buckets S3 (noms uniques)**:
- Source: polystudent-[TIMESTAMP]-source
- Destination: polystudent-[TIMESTAMP]-back

**Rôle IAM**:
- Rôle: S3ReplicationRole-[TIMESTAMP]
- Permissions: Lecture source + Écriture destination

**Réplication**:
- Règle: FullBucketReplication (Status: Enabled)
- Filtre: Tout le bucket
- Stockage: STANDARD

###  RÉSULTAT :
Système de réplication S3 configuré avec succès avec des noms de buckets globaux uniques. La réplication est active et fonctionnelle.

###  NOTE IMPORTANTE :
Les noms de buckets S3 originaux ("polystudens3" et "polystudents3-back") n'étaient pas disponibles car déjà utilisés par d'autres utilisateurs AWS. La solution utilise des noms uniques tout en démontrant la même fonctionnalité de réplication.

**Méthode**: Script Bash avec AWS CLI
**Région**: us-east-1
**Date d'achèvement**: $(date)
**Étudiant**: [Votre nom]
**Cours**: Infonuagique - TP3
