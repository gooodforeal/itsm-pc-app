from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class SCreateIncident(BaseModel):
    user_id: str = Field(..., description="User fio")
    status: str = Field(..., description="Incident status")
    topic: str = Field(..., description="Incident topic")
    description: str = Field(..., description="Incident description")


class SEditIncident(BaseModel):
    incident_id: int = Field(..., description="Incident id")
    status: str = Field(..., description="Incident status")
