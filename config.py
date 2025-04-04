import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Neo4j configuration
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'