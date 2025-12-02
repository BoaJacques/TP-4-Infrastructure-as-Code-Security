# PREUVE D'ACHÈVEMENT - Exercice 3.2
## Configuration VPC avec rôles IAM et alarmes CloudWatch

###  TÂCHES ACCOMPLIES :

1. **Rôle IAM LabRole configuré**
   - Rôle IAM existant réutilisé
   - Politiques CloudWatchFullAccess et AmazonEC2ReadOnlyAccess attachées
   - Instance profile configuré

2. **Architecture VPC déployée**
   - VPC existant utilisé: vpc-0afa78dc6704e5ee8
   - CIDR: 172.31.0.0/16
   - 2 sous-réseaux publics (us-east-1a, us-east-1b)
   - 2 sous-réseaux privés (us-east-1a, us-east-1b)
   - Internet Gateway et tables de routage configurés

3. **4 instances EC2 créées avec succès**
   - Instance Public-AZ1: i-0b29d0934b6100736 (IP: 3.81.200.3) - running
   - Instance Public-AZ2: i-07a1c81d3514e8074 (IP: 44.223.96.165) - pending
   - Instance Private-AZ1: i-004e324e8a615869c - running
   - Instance Private-AZ2: i-08a75c7033099e693 - running
   - Rôle LabRole attaché à toutes les instances
   - Répartition sur deux zones de disponibilité

4. **Alarmes CloudWatch implémentées**
   - 4 alarmes créées (une par instance)
   - Alarmes: HighNetworkIn-Instance-1 à HighNetworkIn-Instance-4
   - Métrique: NetworkPacketsIn
   - Seuil: 1000 paquets/secondes
   - Période: 300 secondes
   - Action: Alarme si dépassement pendant 2 périodes consécutives

###  RÉSULTAT FINAL :
Architecture multi-AZ déployée avec succès avec monitoring CloudWatch actif.

**Composants déployés**:
- 4 instances EC2 (2 publiques, 2 privées)
- 4 sous-réseaux dans 2 AZ
- 4 alarmes CloudWatch configurées
- Rôle IAM LabRole opérationnel

**Configuration technique**:
- Type d'instances: t2.micro
- AMI: ami-0c02fb55956c7d316 (Ubuntu)
- Seuil d'alarme: 1000 pkts/sec
- Période de monitoring: 300 secondes

**Date d'achèvement**: $(date)
**Étudiant**: [Votre nom]
**Cours**: Infonuagique - TP3
**Instance de déploiement**: ip-10-0-0-185
