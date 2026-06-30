# Rendu Séance 5

**Nom et prénom :** GNAZOUYOUFEI Samto<Votre nom complet></votre>

## Résumé de la séance

cluster Spark déployé via Compose, jobs PySpark distribués exécutés, données lues depuis MinIO et résultats écrits en Parquet, comparaison local vs cluster.

1. Déploiement du cluster Spark standalone (1 master + 2 workers) via Docker Compose.
2. Préparation de MinIO et upload du référentiel.
3. Premier job distribué (`analyse_referentiel_cluster.py`) : statistiques de base.
4. Génération d'un historique simulé de trajets et job d'analyse des heures de pointe.
5. Comparaison subjective entre mode local et mode cluster.

## Captures d'écran

### Dashboard Spark Master avec 2 workers

![Spark Master Dashboard](captures/spark-master-dashboard.png)

### Application Spark exécutée avec succès

![Application terminée](captures/spark-app-completed.png)

### Résultats du Top 10 dans la console

![Top 10 heures de pointe](captures/top10-heures-pointe.png)

### Bucket anfa-processed avec heures_de_pointe partitionné

* [ ] ![MinIO heures_de_pointe](captures/minio-heures-pointe.png)

