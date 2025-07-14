from datetime import datetime
from sqlmodel import Field, Session, SQLModel, Column, TIMESTAMP, text, create_engine, select
from typing import Optional

from .schemas import WorkoutPlanBase

class Exercise(SQLModel, table=True):
    exercise_id: int = Field(primary_key=True)
    exercise_name: str

class WorkoutPlan(WorkoutPlanBase, table=True):
    workout_plan_id: int = Field(primary_key=True)
    # reminder: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")))
    exercise: list[Exercise]

class Workout(SQLModel, table=True):
    workout_id: int = Field(primary_key=True)
    workout_plan_id: int = Field(foreign_key="workout.workout_plan_id")
    date: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
    exercises: list[Exercise]
    comment: str = Field(default=None, nullable=True)

class WorkoutExercise(Exercise, table=True):
    workout_exercise_id: int = Field(primary_key=True)
    exercise_id: int = Field(primary_key=True)
    workout_id: int = Field(foreign_key="workout.workout_id")
    name: str
    set: int
    rep: int
    weight: float

class Target(SQLModel, table=True):
    target_id: int = Field(primary_key=True)
    exercise_id: int = Field(foreign_key="exercise.exercise_id")
    set: int
    rep: int
    weight: float
    achieved: bool
    created_at: datetime

class PersonalRecord(SQLModel, table=True):
    personal_record_id: int = Field(primary_key=True)
    exercise_id: int = Field(foreign_key="exercise.exercise_id")