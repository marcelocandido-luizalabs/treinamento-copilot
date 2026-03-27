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

# Business logic functions (testable, no FastAPI dependencies)
def get_activity_by_name(activities_dict, activity_name):
    """Get an activity by name. Raises ValueError if not found."""
    if activity_name not in activities_dict:
        raise ValueError("Activity not found")
    return activities_dict[activity_name]


def add_participant(activities_dict, activity_name, email):
    """Add a participant to an activity.
    
    Raises:
        ValueError: If activity not found, participant already signed up, or activity is full
    """
    activity = get_activity_by_name(activities_dict, activity_name)
    
    if email in activity["participants"]:
        raise ValueError("Student already signed up for this activity")
    
    if len(activity["participants"]) >= activity["max_participants"]:
        raise ValueError("Activity is at maximum capacity")
    
    activity["participants"].append(email)


def remove_participant(activities_dict, activity_name, email):
    """Remove a participant from an activity.
    
    Raises:
        ValueError: If activity not found or participant not signed up
    """
    activity = get_activity_by_name(activities_dict, activity_name)
    
    if email not in activity["participants"]:
        raise ValueError("Student not signed up for this activity")
    
    activity["participants"].remove(email)

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
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
   "Basketball Team": {
      "description": "Competitive basketball training and games",
      "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
      "max_participants": 15,
      "participants": []
   },
   "Swimming Club": {
      "description": "Swimming training and water sports",
      "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
      "max_participants": 20,
      "participants": []
   },
   "Art Studio": {
      "description": "Express creativity through painting and drawing",
      "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
      "max_participants": 15,
      "participants": []
   },
   "Drama Club": {
      "description": "Theater arts and performance training",
      "schedule": "Tuesdays, 4:00 PM - 6:00 PM",
      "max_participants": 25,
      "participants": []
   },
   "Debate Team": {
      "description": "Learn public speaking and argumentation skills",
      "schedule": "Thursdays, 3:30 PM - 5:00 PM",
      "max_participants": 16,
      "participants": []
   },
   "Science Club": {
      "description": "Hands-on experiments and scientific exploration",
      "schedule": "Fridays, 3:30 PM - 5:00 PM",
      "max_participants": 20,
      "participants": []
   }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    try:
        add_participant(activities, activity_name, email)
    except ValueError as e:
        if "Activity not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        elif "already signed up" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        elif "maximum capacity" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Remove a student from an activity"""
    try:
        remove_participant(activities, activity_name, email)
    except ValueError as e:
        if "Activity not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        elif "not signed up" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": f"Unregistered {email} from {activity_name}"}
