"""Pytest configuration and fixtures for activity management tests."""

import pytest


@pytest.fixture
def sample_activities():
    """Provide a fresh copy of sample activities for each test.
    
    This fixture ensures test isolation by creating a new activities dictionary
    for each test, preventing test data pollution from one test to another.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 2,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 3,
            "participants": ["emma@mergington.edu"]
        },
        "Empty Activity": {
            "description": "An empty activity for testing",
            "schedule": "Anytime",
            "max_participants": 5,
            "participants": []
        }
    }


@pytest.fixture
def full_activity():
    """Provide an activity that is at maximum capacity."""
    return {
        "Full Activity": {
            "description": "Activity at max capacity",
            "schedule": "Mondays",
            "max_participants": 1,
            "participants": ["taken@mergington.edu"]
        }
    }
