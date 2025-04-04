from py2neo import Graph
from config import Config

# Initialize Neo4j connection
print("Connecting to Neo4j...")
graph = Graph(Config.NEO4J_URI, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))