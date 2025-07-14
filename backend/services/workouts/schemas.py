from datetime import datetime
from typing import Optional, Annotated

from markdown_it.rules_block import table
from sqlmodel import SQLModel, Field, Column, TIMESTAMP
from .models import Exercise


class WorkoutPlanBase(SQLModel):
    name: str
    description: Optional[str] = Field(default=None, nullable=True)

class WorkoutPlanCreate(WorkoutPlanBase):
    reminder: Optional[datetime] = None # Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")))
    exercise: list[Exercise]

class WorkoutPlanUpdate(WorkoutPlanBase):
    pass