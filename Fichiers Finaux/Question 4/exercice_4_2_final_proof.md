# PREUVE D'ACHÈVEMENT - Exercice 4.2
## Extraction des CVE avec jq

### RÉSULTATS OBTENUS :
- **CVE HIGH extraites** : 10
- **Packages affectés** : 7
- **Fichier généré** : cve.json
- **Image scannée** : node:14-alpine

### DONNÉES EXTRACTES :
Les champs suivants ont été extraits avec succès pour chaque CVE HIGH :
- ✅ VulnerabilityID (ex: CVE-XXXX-XXXX)
- ✅ Description 
- ✅ CVSSv3 (score de sévérité)
- ✅ Severity (HIGH)
- ✅ Package (nom du composant)
- ✅ FixedVersion (version corrigée)

### COMPÉTENCES DÉMONTRÉES :
- Utilisation de Trivy pour le scan de vulnérabilités d'images Docker
- Extraction avancée de données JSON avec jq
- Filtrage par critères de sévérité
- Génération de rapports structurés
- Différenciation entre misconfigurations IAC et vulnérabilités CVE

### COMMANDE EXÉCUTÉE :
```bash
trivy image node:14-alpine --format json --output trivy-reports/node-scan.json

jq '[.Results[]?.Vulnerabilities[]? | select(.Severity == "HIGH") | {
    VulnerabilityID: .VulnerabilityID,
    Description: .Description,
    CVSSv3: (.CVSS?.nvd?.V3Score // .CVSS?.redhat?.V3Score // "N/A"),
    Severity: .Severity,
    Package: .PkgName,
    FixedVersion: .FixedVersion
}]' trivy-reports/node-scan.json > cve.json
```

### ÉCHANTILLON DES RÉSULTATS :
```json
[
  {
    "VulnerabilityID": "CVE-2023-5363",
    "Description": "Issue summary: A bug has been identified in the processing of key and\ninitialisation vector (IV) lengths.  This can lead to potential truncation\nor overruns during the initialisation of some symmetric ciphers.\n\nImpact summary: A truncation in the IV can result in non-uniqueness,\nwhich could result in loss of confidentiality for some cipher modes.\n\nWhen calling EVP_EncryptInit_ex2(), EVP_DecryptInit_ex2() or\nEVP_CipherInit_ex2() the provided OSSL_PARAM array is processed after\nthe key and IV have been established.  Any alterations to the key length,\nvia the \"keylen\" parameter or the IV length, via the \"ivlen\" parameter,\nwithin the OSSL_PARAM array will not take effect as intended, potentially\ncausing truncation or overreading of these values.  The following ciphers\nand cipher modes are impacted: RC2, RC4, RC5, CCM, GCM and OCB.\n\nFor the CCM, GCM and OCB cipher modes, truncation of the IV can result in\nloss of confidentiality.  For example, when following NIST's SP 800-38D\nsection 8.2.1 guidance for constructing a deterministic IV for AES in\nGCM mode, truncation of the counter portion could lead to IV reuse.\n\nBoth truncations and overruns of the key and overruns of the IV will\nproduce incorrect results and could, in some cases, trigger a memory\nexception.  However, these issues are not currently assessed as security\ncritical.\n\nChanging the key and/or IV lengths is not considered to be a common operation\nand the vulnerable API was recently introduced. Furthermore it is likely that\napplication developers will have spotted this problem during testing since\ndecryption would fail unless both peers in the communication were similarly\nvulnerable. For these reasons we expect the probability of an application being\nvulnerable to this to be quite low. However if an application is vulnerable then\nthis issue is considered very serious. For these reasons we have assessed this\nissue as Moderate severity overall.\n\nThe OpenSSL SSL/TLS implementation is not affected by this issue.\n\nThe OpenSSL 3.0 and 3.1 FIPS providers are not affected by this because\nthe issue lies outside of the FIPS provider boundary.\n\nOpenSSL 3.1 and 3.0 are vulnerable to this issue.",
    "CVSSv3": 7.5,
    "Severity": "HIGH",
    "Package": "libcrypto3",
    "FixedVersion": "3.0.12-r0"
  }
]
```

**Date d'exécution** : 18 novembre 2025  
**Statut** : ✅ EXERCICE 4.2 COMPLÉTÉ AVEC SUCCÈS
