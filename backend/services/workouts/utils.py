from fastapi import HTTPException
from sqlmodel import Session
from typing import List
from .database import SessionDependency
from .models import Exercise

def create_exercises(exercises: List[Exercise], session: Session):
    """
    Create multiple Exercise objects in the database and return them.
    
    Args:
        exercises: List of Exercise objects to create.
        session: SQLModel Session for database operations.
    
    Returns:
        List of created Exercise objects with their database-assigned IDs.
    
    Raises:
        HTTPException: If a database error occurs (e.g., duplicate name).
    """
    if not exercises:
        return []
    
    created_exercises = []
    try:
        for exercise in exercises:
            session.add(exercise)
            created_exercises.append(exercise)
        session.commit()
        for exercise in created_exercises:
            session.refresh(exercise)
        return created_exercises
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating exercises: {str(e)}")