"""Unit tests for activity management business logic using AAA pattern.

These tests focus on error scenarios and edge cases for the activity management
functions. Each test follows the Arrange-Act-Assert pattern for clarity.
"""

import pytest
from src.app import get_activity_by_name, add_participant, remove_participant


class TestGetActivityByName:
    """Tests for get_activity_by_name function."""
    
    def test_activity_not_found_raises_value_error(self, sample_activities):
        """Test that requesting a non-existent activity raises ValueError.
        
        Arrange: Create activities dict without a specific activity
        Act: Try to get a non-existent activity
        Assert: Verify ValueError is raised with correct message
        """
        # Arrange
        activities = sample_activities
        activity_name = "Non-existent Activity"
        
        # Act & Assert
        with pytest.raises(ValueError, match="Activity not found"):
            get_activity_by_name(activities, activity_name)
    
    def test_activity_found_returns_correct_activity(self, sample_activities):
        """Test that requesting an existing activity returns its data.
        
        Arrange: Create activities dict with known activity
        Act: Get an existing activity
        Assert: Verify the returned activity data is correct
        """
        # Arrange
        activities = sample_activities
        activity_name = "Chess Club"
        expected_activity = activities["Chess Club"]
        
        # Act
        result = get_activity_by_name(activities, activity_name)
        
        # Assert
        assert result == expected_activity
        assert result["max_participants"] == 2
        assert "michael@mergington.edu" in result["participants"]


class TestAddParticipant:
    """Tests for add_participant function."""
    
    def test_add_to_nonexistent_activity_raises_value_error(self, sample_activities):
        """Test that adding to a non-existent activity raises ValueError.
        
        Arrange: Create activities dict without target activity
        Act: Try to add participant to non-existent activity
        Assert: Verify ValueError is raised with 'Activity not found' message
        """
        # Arrange
        activities = sample_activities
        activity_name = "Non-existent Activity"
        email = "student@mergington.edu"
        
        # Act & Assert
        with pytest.raises(ValueError, match="Activity not found"):
            add_participant(activities, activity_name, email)
    
    def test_add_duplicate_participant_raises_value_error(self, sample_activities):
        """Test that adding an already-registered participant raises ValueError.
        
        Arrange: Activity with existing participant
        Act: Try to add the same participant again
        Assert: Verify ValueError is raised with duplicate message
        """
        # Arrange
        activities = sample_activities
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act & Assert
        with pytest.raises(ValueError, match="already signed up"):
            add_participant(activities, activity_name, email)
    
    def test_add_to_full_activity_raises_value_error(self, full_activity):
        """Test that adding to a full activity raises ValueError.
        
        Arrange: Activity at maximum capacity
        Act: Try to add participant to full activity
        Assert: Verify ValueError is raised with capacity message
        """
        # Arrange
        activities = full_activity
        activity_name = "Full Activity"
        email = "newstudent@mergington.edu"
        
        # Act & Assert
        with pytest.raises(ValueError, match="maximum capacity"):
            add_participant(activities, activity_name, email)
    
    def test_add_participant_success(self, sample_activities):
        """Test successfully adding a new participant to an activity.
        
        Arrange: Activity with available spot and new email
        Act: Add participant to activity
        Assert: Verify participant is added and count increases
        """
        # Arrange
        activities = sample_activities
        activity_name = "Programming Class"
        email = "newstudent@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])
        
        # Act
        add_participant(activities, activity_name, email)
        
        # Assert
        assert email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count + 1
    
    def test_add_to_empty_activity(self, sample_activities):
        """Test adding first participant to an empty activity.
        
        Arrange: Empty activity with available capacity
        Act: Add first participant
        Assert: Verify participant is added successfully
        """
        # Arrange
        activities = sample_activities
        activity_name = "Empty Activity"
        email = "firstuser@mergington.edu"
        
        # Act
        add_participant(activities, activity_name, email)
        
        # Assert
        assert email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == 1


class TestRemoveParticipant:
    """Tests for remove_participant function."""
    
    def test_remove_from_nonexistent_activity_raises_value_error(self, sample_activities):
        """Test that removing from non-existent activity raises ValueError.
        
        Arrange: Create activities dict without target activity
        Act: Try to remove from non-existent activity
        Assert: Verify ValueError is raised with 'Activity not found' message
        """
        # Arrange
        activities = sample_activities
        activity_name = "Non-existent Activity"
        email = "student@mergington.edu"
        
        # Act & Assert
        with pytest.raises(ValueError, match="Activity not found"):
            remove_participant(activities, activity_name, email)
    
    def test_remove_participant_not_signed_up_raises_value_error(self, sample_activities):
        """Test that removing a non-registered participant raises ValueError.
        
        Arrange: Activity without target participant
        Act: Try to remove participant not in activity
        Assert: Verify ValueError is raised with 'not signed up' message
        """
        # Arrange
        activities = sample_activities
        activity_name = "Chess Club"
        email = "notsignedupstudent@mergington.edu"
        
        # Act & Assert
        with pytest.raises(ValueError, match="not signed up"):
            remove_participant(activities, activity_name, email)
    
    def test_remove_participant_success(self, sample_activities):
        """Test successfully removing a participant from an activity.
        
        Arrange: Activity with existing participant
        Act: Remove the participant
        Assert: Verify participant is removed and count decreases
        """
        # Arrange
        activities = sample_activities
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])
        
        # Act
        remove_participant(activities, activity_name, email)
        
        # Assert
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1
    
    def test_remove_participant_from_activity_with_multiple(self, sample_activities):
        """Test removing one participant from activity with multiple participants.
        
        Arrange: Activity with multiple participants
        Act: Remove one specific participant
        Assert: Verify only target participant is removed
        """
        # Arrange
        activities = sample_activities
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"
        other_email = "michael@mergington.edu"
        
        # Act
        remove_participant(activities, activity_name, email)
        
        # Assert
        assert email not in activities[activity_name]["participants"]
        assert other_email in activities[activity_name]["participants"]
