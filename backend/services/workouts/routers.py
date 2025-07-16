from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select, Session
from .models import WorkoutPlan, Exercise, WorkoutPlanCreate, WorkoutPlanPublic
from .database import SessionDependency, engine
from .utils import create_exercises

router = APIRouter(
    prefix="/workouts"
)

exercises_list = [
    Exercise(name="Bicep curls"),
    Exercise(name="Deadlift"),
    Exercise(name="Squats"),
]

create_exercises(exercises_list, session = Session(engine))

@router.post("/workout-plan", response_model=WorkoutPlanPublic)
def create_workout_plan(workout_plan: WorkoutPlanCreate, session: SessionDependency):

    # Fetch actual Exercise instances from DB
    if workout_plan.exercises:
        exercises = session.exec(select(Exercise).where(Exercise.id.in_(workout_plan.exercises))).all() # type: ignore
        
        if len(exercises) != len(workout_plan.exercises):
            raise HTTPException(status_code=400, detail="One or more exercise IDs are invalid.")

        # Convert WorkoutPlanCreate into a plain WorkoutPlan without exercises
    db_workout_plan = WorkoutPlan(
            name=workout_plan.name,
            description=workout_plan.description,
            reminder=workout_plan.reminder,
            exercises = list(exercises),
        )

    session.add(db_workout_plan)
    session.commit()
    session.refresh(db_workout_plan)
    return db_workout_plan

@router.get("/workout-plan", response_model=list[WorkoutPlanPublic])
async def read_workout_plans(
        session: SessionDependency,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    workout_plans = session.exec(select(WorkoutPlan).offset(offset).limit(limit)).all()

    if workout_plans is None:
        raise HTTPException(status_code=404, detail="Workout plans not found")
    return workout_plans

@router.get("/workout-plan/{workout_plan_id}", response_model=WorkoutPlanPublic)
async def read_workout_plan(workout_plan_id: int, session: SessionDependency):
    workout_plan = session.get(WorkoutPlan, workout_plan_id)

    if workout_plan is None:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    return workout_plan


@router.patch("/workout-plan/{workout_plan_id}", response_model=WorkoutPlanPublic)
async def update_workout_plan(workout_plan_id : int, plan: WorkoutPlanCreate, session: SessionDependency):
    workout_plan = session.get(WorkoutPlan, workout_plan_id)

    if workout_plan is None:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    
    # Update scalar fields
    workout_plan_data = plan.model_dump(exclude_unset=True)
    workout_plan.sqlmodel_update(workout_plan_data)

    # Handle exercises update manually
    if plan.exercises:
        # Fetch actual Exercise objects
        exercises = session.exec(
            select(Exercise).where(Exercise.id.in_(plan.exercises)) # type: ignore
        ).all()

        if len(exercises) != len(plan.exercises):
            raise HTTPException(status_code=400, detail="Some exercise IDs are invalid.")

        # Replace the relationship
        workout_plan.exercises = list(exercises)

    session.add(workout_plan)
    session.commit()
    session.refresh(workout_plan)
    return workout_plan

@router.delete("/workout-plan/{workout_plan_id}")
async def delete_workout_plan(workout_plan_id: int, session: SessionDependency):
    workout_plan = session.get(WorkoutPlan, workout_plan_id)
    if workout_plan is None:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    session.delete(workout_plan)
    session.commit()
    return {"status": "deleted"}

