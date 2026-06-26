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



## Réponses aux exercices d'application

## Exercice 1 : QCM 

**1.1 — Réponse : C.** Un conteneur partage le noyau de la machine hôte (contrairement à une VM qui embarque son propre noyau et un OS complet).

**1.2 — Réponse : B.** L'image est un modèle figé en lecture seule (un  *template* ) ; le conteneur est une instance vivante de cette image, avec une couche d'écriture par-dessus.

**1.3 — Réponse : B.** Docker utilise les *namespaces* du noyau Linux pour cloisonner ce que voit chaque conteneur (PID, réseau, montages, etc.).

**1.4 — Réponse : A.** Les *cgroups* (control groups) servent à plafonner et compter les ressources (CPU, mémoire, I/O) consommées par un conteneur.

**1.5 — Réponse : B.** macOS n'étant pas Linux, Docker Desktop lance une machine virtuelle Linux légère et invisible dans laquelle tournent réellement les conteneurs.

**1.6 — Réponse : B.** DotCloud était la société (un PaaS) qui a développé Docker en interne puis l'a open-sourcé en 2013, avant de se renommer Docker, Inc.

**1.7 — Réponse : C.** Sur les mêmes primitives noyau que LXC (namespaces, cgroups), Docker a apporté un format d'image portable, une CLI simple et un registre public, démocratisant ainsi les conteneurs.

**1.8 — Réponse : B.** OCI =  *Open Container Initiative* , la norme ouverte qui standardise le format des images et le runtime des conteneurs.


## Exercice 2 : Lecture et analyse d'un Dockerfile

### 2.1 Rôle de chaque instruction

* `FROM python:3.11` — définit l'image de base (Debian + Python 3.11) sur laquelle l'image est construite.
* `WORKDIR /application` — fixe (et crée si besoin) le répertoire de travail dans lequel s'exécutent les instructions suivantes.
* `COPY . /application` — copie tout le contexte de build (le contenu du dossier courant) dans `/application` de l'image.
* `RUN pip install -r requirements.txt` — installe, au moment du build, les dépendances Python listées dans `requirements.txt`.
* `EXPOSE 5000` — documente que l'application écoute sur le port 5000 (métadonnée uniquement).
* `CMD ["python", "main.py"]` — définit la commande exécutée par défaut au démarrage d'un conteneur issu de l'image.

### 2.2 `EXPOSE 5000` vs `-p 5000:5000`

`EXPOSE` est purement **déclaratif/documentaire** : il indique le port d'écoute mais n'ouvre rien et ne rend le service accessible ni depuis l'hôte ni depuis l'extérieur. `-p 5000:5000` **publie réellement** le port en mappant le port 5000 de l'hôte sur le port 5000 du conteneur, rendant l'application joignable. Sans `-p` (ou `-P`), `EXPOSE` seul ne suffit pas à atteindre le conteneur depuis la machine hôte.

### 2.3 Deux problèmes (bonnes pratiques)

**Problème 1 — Image de base trop lourde.**
`python:3.11` est une image volumineuse (~1 Go, Debian complet). *Correction :* utiliser une variante allégée comme `python:3.11-slim`, qui suffit pour la plupart des applications et réduit fortement la taille et la surface d'attaque.

**Problème 2 — Mauvais ordre, cache de build cassé.**
`COPY . /application` est placé **avant** `RUN pip install`. Du coup, la moindre modification d'un fichier source invalide le cache et force une réinstallation complète des dépendances à chaque build. *Correction :* copier d'abord `requirements.txt`, lancer `pip install`, puis copier le reste du code.

*(Problème supplémentaire défendable : le conteneur tourne en `root` — voir la correction en 2.4 avec un utilisateur non privilégié.)*

### 2.4 Version corrigée du Dockerfile



FROM python:3.11-slim

# Créer un utilisateur non-root

RUN useradd --create-home appuser

WORKDIR /application

# Copier d'abord les dépendances pour maximiser le cache

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Puis copier le reste du code

COPY . .

# Exécuter sous l'utilisateur non privilégié

USER appuser

EXPOSE 5000

CMD ["python", "main.py"]


Cette version applique : **image de base plus légère** (`slim`), **ordre optimisant le cache** (`requirements.txt` avant le code source), **utilisateur non-root** (`appuser`). Le `--no-cache-dir` évite en plus de garder le cache pip dans l'image.



## Exercice 3 : Diagnostic

### 3.1 Le build qui échoue

**a. Cause précise.**
`RUN pip install -r requirements.txt` s'exécute **avant** `COPY . .`. À cette étape, aucun fichier du contexte de build n'a encore été copié dans l'image : `/app/requirements.txt` n'existe pas, donc pip ne trouve pas le fichier (`No such file or directory`).

**b. Correction.** Copier les fichiers (au minimum `requirements.txt`) **avant** d'installer :

dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

**c. Pourquoi cela traduit une mauvaise compréhension de Docker.**
Chaque instruction du Dockerfile s'exécute  **séquentiellement** , dans des couches isolées, et le système de fichiers de l'image ne contient que ce que les instructions précédentes y ont mis. Les fichiers de l'hôte (le contexte de build) ne sont **pas** disponibles automatiquement : ils n'apparaissent dans l'image qu'après un `COPY`/`ADD`. L'étudiant a raisonné comme s'il était sur sa machine locale (où tous les fichiers sont déjà là), au lieu de raisonner en couches successives propres au build Docker.

### 3.2 Le conteneur qui ne voit pas l'autre

**a. Erreur dans `DATABASE_URL`.**
Le hôte est `localhost`. Or, dans Docker Compose, chaque service a son propre espace réseau : à l'intérieur du conteneur `api`, `localhost` désigne `api` lui-même, où aucune base Postgres ne tourne — d'où le `connection refused`. Les services se joignent entre eux par leur **nom de service** sur le réseau Compose.

**b. Correction.** Remplacer `localhost` par le nom du service de base de données, `db` :

yaml

```yaml
DATABASE_URL:"postgresql://user:password@db:5432/anfa"
```




## Exercice 4 : Optimisation d'image

### a. Au moins quatre problèmes

1. **Image de base trop générique et lourde** — `ubuntu:22.04` impose d'installer Python à la main ; `python:3.11-slim` ferait le même travail pour une image bien plus petite. *(taille)*
2. **`RUN apt-get` multiples sans nettoyage** — plusieurs couches d'installation, et aucun `apt-get clean` / `rm -rf /var/lib/apt/lists/*` : le cache et les métadonnées apt gonflent l'image. *(taille / hygiène)*
3. **Outils inutiles au runtime** — `build-essential`, `git`, `curl`, `wget` ne servent pas à un simple script utilisant `requests` : centaines de Mo gaspillées et surface d'attaque accrue. *(taille / sécurité)*
4. **`COPY . /app` avant `pip install` + pas de `--no-cache-dir`** — toute modification du code invalide le cache et réinstalle les dépendances ; le cache pip reste en plus dans l'image. *(cache / taille)*
5. *(bonus)* **Exécution en `root`** — aucun utilisateur non privilégié n'est défini. *(sécurité)*
6. *(bonus)* **`apt-get update` séparé de l'install** — risque de listes de paquets périmées (cache de couche) et builds non reproductibles. *(hygiène)*


## Exercice 5 : Mini-cas d'architecture

### a. Services à conteneuriser

* **`minio`** — stockage objet compatible S3 ; héberge le bucket où sont écrits les résultats nettoyés et agrégés.
* **`pipeline`** (le script Python) — job batch qui lit les positions GPS depuis le FTP, les nettoie/agrège et écrit le résultat dans MinIO ; lancé chaque nuit ou à la demande pour un rejeu.
* **`jupyter`** — environnement de notebooks pour Kossi et Awa, afin d'explorer les données de MinIO et produire des graphiques.
* **`minio-init`** *(optionnel)* — petit conteneur jetable (client `mc`) qui crée le bucket au premier démarrage.

> Le **dépôt FTP** est une source externe existante : on s'y connecte, on ne le conteneurise pas (sauf un faux FTP local en dev). La **planification nocturne** peut être assurée par un `cron` de l'hôte qui lance `docker compose run pipeline`, ou par un ordonnanceur dédié (cron-container, voire Airflow) si le besoin se complexifie.

### b. Restart policy du script Python (FTP)

Je choisis **`on-failure`** (éventuellement `on-failure:3`). Ce script est un **job batch** qui s'exécute puis se termine (`exit 0`) ; `always` ou `unless-stopped` le relanceraient en boucle infinie après chaque fin réussie. `on-failure` ne relance qu'en cas de sortie en erreur, ce qui couvre les pannes transitoires (FTP/réseau indisponible) sans rejouer le traitement quand il a réussi. *(`no` reste défendable si l'on confie entièrement les reprises à l'ordonnanceur.)*

### c. Passer la date au script pour un rejeu

Deux mécanismes Docker, sans toucher au code Python (en supposant que le script sait lire une date) :

1. **Variable d'environnement** : `docker compose run -e RUN_DATE=2025-06-01 pipeline`. Le script lit `RUN_DATE` ; si elle est absente, il prend la date du jour par défaut.
2. **Override des arguments de la commande** : `docker compose run pipeline python downloader.py --date 2025-06-01`. On remplace les arguments du `CMD` au lancement.

**Recommandation : la variable d'environnement.** C'est l'approche la plus idiomatique (config dans l'environnement, principe  *12-factor* ), naturelle avec Compose : le run nocturne laisse `RUN_DATE` vide → date du jour, et un rejeu ne nécessite que de fixer `RUN_DATE` à la date voulue, sans modifier l'entrypoint.

### d. « Pourquoi pas le script dans le conteneur Jupyter ? »

Parce que les deux ont des **cycles de vie et des besoins différents** : le pipeline est un job batch qui s'exécute, échoue/réussit, se planifie et se rejoue  **indépendamment** , alors que Jupyter est un serveur interactif qui doit rester allumé. Les coupler signifierait que le pipeline ne tourne que si le notebook est ouvert, rendrait planification et rejeu compliqués, et opposerait des politiques de redémarrage incompatibles (`always` pour Jupyter, `on-failure` pour le batch). Côté  **reproductibilité et déploiement** , une image pipeline dédiée est plus légère, testable et exécutable en cron/CI/production sans embarquer toute la pile Jupyter. On garde donc chaque responsabilité isolée.

### e. Squelette `docker-compose.yml`



version: "3.8"

services:
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"   # API S3
      - "9001:9001"   # console web
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: password
    volumes:
      - minio-data:/data

  pipeline:
    build: ./pipeline
    environment:
      RUN_DATE: "${RUN_DATE:-}"        # vide = aujourd'hui ; fixée = rejeu d'un jour
      MINIO_ENDPOINT: "minio:9000"
      FTP_HOST: "ftp.anfa.example"
    depends_on:
      - minio
    restart: on-failure

  jupyter:
    build: ./jupyter                   # ou image: jupyter/minimal-notebook
    ports:
      - "8888:8888"
    depends_on:
      - minio
    volumes:
      - ./notebooks:/home/jovyan/work

volumes:
  minio-data:

## Difficultés rencontrées

* [ ] la taille des deux image sont les meme apres le multistage
