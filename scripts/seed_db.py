"""Popula o MongoDB local com as atividades hardcoded do projeto.

Este script insere documentos na coleção `activities` usando o nome da
atividade como chave `_id` e mantendo a estrutura existente.
"""
import json
from pathlib import Path
from pymongo import MongoClient
import os

ROOT = Path(__file__).parent.parent
APP = ROOT / 'src' / 'app.py'

# Para evitar executar o código da aplicação durante o seed, definimos aqui
# o mesmo dicionário de activities que existia anteriormente.
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in local leagues",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Practice basketball skills and play friendly matches",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act in plays and participate in theater productions",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore painting, drawing, and sculpture",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["amelia@mergington.edu", "benjamin@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Prepare for math competitions and solve challenging problems",
        "schedule": "Fridays, 2:00 PM - 3:30 PM",
        "max_participants": 15,
        "participants": ["charlotte@mergington.edu", "elijah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["harper@mergington.edu", "james@mergington.edu"]
    }
}

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('MONGO_DB', 'mergington')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
coll = db.activities

print('Limpando coleção activities...')
coll.delete_many({})

docs = []
for name, details in activities.items():
    doc = details.copy()
    doc['_id'] = name
    docs.append(doc)

if docs:
    coll.insert_many(docs)
    print(f'Inseridas {len(docs)} atividades na coleção activities do DB "{DB_NAME}"')
else:
    print('Nenhuma atividade encontrada para inserir')

print('Concluído')
