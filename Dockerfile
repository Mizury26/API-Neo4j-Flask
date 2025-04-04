FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Exposer le port utilisé par l'application
EXPOSE 5000

# Créer un utilisateur non-root pour la sécurité
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Commande pour démarrer l'application
CMD ["python", "app.py"]