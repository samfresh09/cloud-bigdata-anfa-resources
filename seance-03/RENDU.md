
# Rendu Séance 3

**Nom et prénom :** <Votre nom complet></votre> GNAZOUYOUFEI Samto
**Identifiant GitHub :** <votre-username></votre>Samfresh09
**Date de soumission :** 26-06-2026

## Résumé de la séance

Kind installé, cluster Kubernetes créé

namespace anfa configuré, MinIO déployé via 3 manifestes YAML

* [ ]  self-healing observé, scaling testé, Ingress Controller activé.

## Étapes principales

1. Installation de Kind et kubectl, création du cluster `anfa`.
2. Création du namespace `anfa` et configuration de kubectl.
3. Déploiement de MinIO via 3 manifestes YAML (PVC, Deployment, Service).
4. Observation du self-healing après suppression manuelle d'un pod.
5. Scaling du Deployment de 1 à 3 replicas, puis retour à 1.
6. Activation de l'Ingress Controller nginx.

## Captures d'écran

### Console MinIO accessible via port-forward

![Console MinIO](captures/console-minio.png)

### Self-healing observé

![Pod recréé](captures/self-healing.png)

### Scaling à 3 replicas

![3 replicas MinIO](captures/scaling-3-replicas.png)

## Réponses aux exercices d'application

<À compléter d'après les énoncés fournis avec l'assignment.>

## Difficultés rencontrées

<Aucune | Décrivez brièvement.>
