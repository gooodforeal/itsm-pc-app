from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class SUserCheck(BaseModel):
    key: str = Field(..., description="Session key")


class SBuildUser(BaseModel):
    id: int = Field(..., description="User id")
    fio: str = Field(..., description="Users fio")


class SBuildClient(BaseModel):
    id: int = Field(..., description="Client id")
    fio: str = Field(..., description="Clients fio")


class SComponent(BaseModel):
    title: str = Field(..., description="Component title")


class SBuildCreate(SUserCheck):
    client: str = Field(..., description="Clients fio")
    components: List[SComponent]


class SBuild(BaseModel):
    id: int = Field(..., description="Build id")
    created_at: datetime = Field(..., description="Build creation date")
    user: SBuildUser
    client: SBuildUser


class SGetBuild(SUserCheck):
    id: int = Field(..., description="Build id")


