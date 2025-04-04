# ⚙️ API - Flask Neo4j

Project by __ARCAS__ Manon

This project provides a web RESTful API built with Flask and Neo4j database.

This README will guide you through setting up your environment, installing the required packages, and starting the project.

## 📌 Table of Contents


I. [Badges](#🎯-badges)

II. [Prerequisites](#🔧-prerequisites)

III. [Availables Features](#💡-availables-features)

IV. [Endpoints](#📋-endpoints)

V. [Installing the project](#💻-project-installation)

VI. [Docker installation](#💻-use-docker-for-the-project )

## 🎯 Badges

![Python](https://img.shields.io/badge/Python-008020?style=flat&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) ![Neo4j](https://img.shields.io/badge/Neo4j-4581C3?style=flat&logo=neo4j&logoColor=white)
 ![Docker](https://img.shields.io/badge/Docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white) ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=flat&logo=postman&logoColor=white)

## 🔧 Prerequisites :

- [Python](https://www.python.org) installed on your system.
- [Docker](https://www.docker.com) installed on your system.

## 💡 Availables Features :

This solution provides a web API in Python using Flask and Neo4j. The API offers a CRUD system for user, post and comment/like . The different routes are detailed below.

## 📋 Endpoints :

### User :

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET     | /users | Récupérer la liste des utilisateurs |
| POST    | /users | Créer un nouvel utilisateur |
| GET     | /users/:id | Récupérer un utilisateur par son ID |
| PUT     | /users/:id | Mettre à jour un utilisateur par son ID |
| DELETE  | /users/:id | Supprimer un utilisateur par son ID |
| GET     | /users/:id/friends | Récupérer la liste des amis d'un utilisateur |
| POST    | /users/:id/friends | Ajouter un ami (ID de l'ami dans le body) |
| DELETE  | /users/:id/friends/:friendId | Supprimer un ami |
| GET     | /users/:id/friends/:friendId | Vérifier si deux utilisateurs sont amis |
| GET     | /users/:id/mutual-friends/:otherId | Récupérer les amis en commun |

---

### Posts :

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET     | /posts | Récupérer tous les posts |
| GET     | /posts/:id | Récupérer un post par son ID |
| GET     | /users/:id/posts | Récupérer les posts d'un utilisateur |
| POST    | /users/:id/posts | Créer un post (lié au créateur via une relation CREATED) |
| PUT     | /posts/:id | Mettre à jour un post |
| DELETE  | /posts/:id | Supprimer un post |
| POST    | /posts/:id/like | Ajouter un like à un post (relation LIKES entre un utilisateur et le post) |
| DELETE  | /posts/:id/like | Retirer un like d'un post (supprimer la relation LIKES) |

---

### Comment :

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET     | /posts/:id/comments | Récupérer les commentaires d'un post |
| POST    | /posts/:id/comments | Ajouter un commentaire (relations CREATED avec l'utilisateur et HAS_COMMENT avec le post) |
| DELETE  | /posts/:postId/comments/:commentId | Supprimer un commentaire d'un post |
| GET     | /comments | Récupérer tous les commentaires |
| GET     | /comments/:id | Récupérer un commentaire par son ID |
| PUT     | /comments/:id | Mettre à jour un commentaire |
| DELETE  | /comments/:id | Supprimer un commentaire |
| POST    | /comments/:id/like | Ajouter un like à un commentaire (relation LIKES entre un utilisateur et le commentaire) |
| DELETE  | /comments/:id/like | Retirer un like d'un commentaire (supprimer la relation LIKES) |



## 💻 Project Installation :

1. Clone the Repository

```bash
git clone https://github.com/Mizury26/API-Neo4j-Flask.git
```

#### 2. Navigate to the Project Directory :
```bash
cd API-Neo4j-Flask
```

### 3. Create a Virtual Environment
```bash
python3 -m venv venv
```

### 4. Activate the Virtual Environment
#### On Windows:
```bash
venv\Scripts\activate
```
#### On macOS and Linux:
```bash
source venv/bin/activate
```
### 5. Install Required Packages
```bash
pip install -r requirements.txt
```

#### 5. Configure environments variables  :
Complete the .env file with your configuration.<br>
You can use [this](.env.example) template.

#### 6. Start the project :
```bash
py app.py
```

## 💻 Use Docker for the project :

#### 1. Clone the Repository :
```bash
git clone https://github.com/Mizury26/API-Neo4j-Flask.git
```

#### 2. Navigate to the Project Directory :
```bash
cd API-Neo4j-Flask
```

#### 3. Configure environments variables  :
Complete the .env file (example [here](.env.example)) with your configuration. Attention, you need to add the container name of the database instead of the ip and take care of adding the correct credentials (the same as in the [docker compose](./docker-compose.yml))

#### 3. Build the Docker Image :
```bash
docker-compose up -d
```

### Access the API :
Visit http://localhost:5000 in your web browser to access the API.


**✅ Congratulation ! Your API is now available**

You can test it with [Postman](https://www.postman.com) or on your browser directly.
You can also execute the [test script](./test.py)