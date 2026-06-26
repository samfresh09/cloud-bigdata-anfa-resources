# Rendu - Séance 2

**Nom et prénom :** GNAZOUYOUFEI SAMTO

**Identifiant GitHub :**  Samfresh09

**Date de soumission :** 26-06-2026

## Résumé de la séance

 Dockerfile écrit, 

image construite et exécutée, 

stack Compose à 3 services orchestrée

 notebook Jupyter lisant MinIO.

## Étapes principales

1. Écriture du Dockerfile et construction de l'image `anfa-analyse:v1` (1.17GB).
2. Mise en place du `.dockerignore` et observation du cache de Docker.
3. Écriture du `docker-compose.yml` orchestrant MinIO, Jupyter, et l'image custom.
4. Création du notebook `exploration_minio.ipynb` qui lit les données depuis MinIO via boto3 et pandas.

## Bonus multi-stage (optionnel)

anfa-analyse             v2-multistage                  10a006e2f3c8   3 days ago      1.17GB

## Difficultés rencontrées

* [ ] la taille des deux image sont les meme apres le multistage
