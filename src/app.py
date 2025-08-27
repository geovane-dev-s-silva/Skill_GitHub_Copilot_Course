"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from pymongo import MongoClient
from bson.objectid import ObjectId
from .db import get_activities_collection

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# NOTE: activities will be stored in MongoDB. When the server starts, if the
# collection is empty the developer can run `scripts/seed_db.py` to populate it
# with the original hard-coded activities.


def _activities_from_db():
    """Returna todas as atividades como um dict com o nome como chave."""
    coll = get_activities_collection()
    res = {}
    for doc in coll.find():
        key = doc.get('_id')
        # remove internal _id from the payload
        d = {k: v for k, v in doc.items() if k != '_id'}
        res[key] = d
    return res


# Compatibility: leave original in-memory var for tests that might import it
activities = _activities_from_db()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    # Re-read from DB on each request to keep things simple for this demo
    return _activities_from_db()


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    coll = get_activities_collection()
    doc = coll.find_one({"_id": activity_name})
    if not doc:
        raise HTTPException(status_code=404, detail="Activity not found")

    participants = doc.get('participants', [])
    if email in participants:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    participants.append(email)
    coll.update_one({"_id": activity_name}, {"$set": {"participants": participants}})
    return {"message": f"Signed up {email} for {activity_name}"}


# Novo endpoint para remover participante
from fastapi import Query

@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str = Query(...)):
    """Remove um participante de uma atividade"""
    coll = get_activities_collection()
    doc = coll.find_one({"_id": activity_name})
    if not doc:
        raise HTTPException(status_code=404, detail="Activity not found")
    participants = doc.get('participants', [])
    if email not in participants:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")
    participants.remove(email)
    coll.update_one({"_id": activity_name}, {"$set": {"participants": participants}})
    return {"message": f"{email} removido de {activity_name}"}
