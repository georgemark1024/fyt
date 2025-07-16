from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List

class WorkoutPlanBase(SQLModel):
    name: str
    description: Optional[str] = Field(default=None, nullable=True)

# Junction table for WorkoutPlan-Exercise (many-to-many)
class WorkoutPlanExercise(SQLModel, table=True):
    workout_plan_id: Optional[int] = Field(
        default=None, foreign_key="workoutplan.id", primary_key=True
    )
    exercise_id: Optional[int] = Field(
        default=None, foreign_key="exercise.id", primary_key=True
    )

class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    workout_plans: List["WorkoutPlan"] = Relationship(back_populates="exercises", link_model=WorkoutPlanExercise)
    workout_exercises: List["WorkoutExercise"] = Relationship(back_populates="exercise")

class WorkoutPlan(WorkoutPlanBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reminder: Optional[datetime] = Field(default=None, nullable=True)
    
    # Relationship to Exercises via the junction table
    exercises: List[Exercise] = Relationship(
        back_populates="workout_plans", link_model=WorkoutPlanExercise
    )
    # Relationship to Workouts
    workouts: List["Workout"] = Relationship(back_populates="workout_plan")

# Workout model (a gym session based on a WorkoutPlan)
class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    workout_plan_id: Optional[int] = Field(
        default=None, foreign_key="workoutplan.id"
    )
    date: Optional[datetime] = Field(default=None, nullable=True)
    comment: str = Field(default=None, nullable=True)

    # Relationships
    workout_plan: Optional[WorkoutPlan] = Relationship(back_populates="workouts")
    workout_exercises: List["WorkoutExercise"] = Relationship(back_populates="workout")

class WorkoutExercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exercise_id: Optional[int] = Field(default=None, foreign_key="exercise.id")
    workout_id: Optional[int] = Field(default=None, foreign_key="workout.id")
    set: int
    rep: int
    weight: Optional[float] = Field(default=None, nullable=True)

    # Relationships
    workout: Optional[Workout] = Relationship(back_populates="workout_exercises")
    exercise: Optional[Exercise] = Relationship(back_populates="workout_exercises")

class Target(SQLModel, table=True):
    target_id: int = Field(primary_key=True)
    exercise_id: int = Field(foreign_key="exercise.id")
    set: int
    rep: int
    weight: float
    achieved: bool
    created_at: datetime

class PersonalRecord(SQLModel, table=True):
    personal_record_id: int = Field(primary_key=True)
    exercise_id: int = Field(foreign_key="exercise.id")

class WorkoutPlanCreate(WorkoutPlanBase):
    reminder: Optional[datetime] = None
    exercises: list[int]

class WorkoutPlanPublic(WorkoutPlanBase):
    reminder: Optional[datetime] = None
    exercises: list[Exercise]

class WorkoutPlanUpdate(WorkoutPlanBase):
    pass