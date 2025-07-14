from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from .models import WorkoutPlan
from .database import SessionDependency

router = APIRouter(
    prefix="/workouts"
)

@router.post("/workout-plan", response_model=WorkoutPlan)
def create_workout_plan(workout_plan: WorkoutPlan, session: SessionDependency) -> WorkoutPlan:
    session.add(workout_plan)
    session.commit()
    session.refresh(workout_plan)
    return workout_plan

@router.get("/workout-plan", response_model=WorkoutPlan)
async def read_workout_plans(
        session: SessionDependency,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) -> list[WorkoutPlan]:
    workout_plans = session.exec(select(WorkoutPlan).offset(offset).limit(limit)).all()

    if workout_plans is None:
        raise HTTPException(status_code=404, detail="Workout plans not found")
    return workout_plans

@router.get("/workout-plan/{workout_plan_id}", response_model=WorkoutPlan)
async def read_workout_plan(workout_plan_id: int, session: SessionDependency) -> WorkoutPlan:
    workout_plan = session.get(WorkoutPlan, workout_plan_id)

    if workout_plan is None:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    return workout_plan


@router.patch("/workout-plan/{workout_plan_id}", response_model=WorkoutPlan)
async def update_workout_plan(workout_plan_id : int, workout_plan: WorkoutPlan, session: SessionDependency) -> WorkoutPlan:
    workout_plan = session.get(WorkoutPlan, workout_plan_id)

    if workout_plan is None:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    workout_plan_data = workout_plan.model_dump(exclude_unset=True)
    workout_plan.sqlmodel_update(workout_plan_data)
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

