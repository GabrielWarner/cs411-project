from pymongo import MongoClient
from datetime import datetime

# 1) Connect to your local MongoDB (adjust URI/db name as needed)
_client = MongoClient("mongodb://localhost:27017")
_db     = _client["academicworld"]       # your Mongo database
_notes  = _db["faculty_notes"]           # new collection for notes

def get_notes_for_faculty(faculty_name: str):
    """
    Fetch all notes for that faculty, newest first.
    Returns a list of dicts: { text: str, time: datetime }.
    """
    docs = _notes.find({"faculty": faculty_name}).sort("timestamp", -1)
    return [{"text": d["text"], "time": d["timestamp"]} for d in docs]

def add_note_for_faculty(faculty_name: str, note_text: str):
    """
    Insert a new note document with UTC timestamp.
    """
    if not note_text.strip():
        return
    doc = {
        "faculty":   faculty_name,
        "text":      note_text.strip(),
        "timestamp": datetime.utcnow()
    }
    _notes.insert_one(doc)