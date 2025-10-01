from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class Commander(BaseModel):
    id: int = Field(..., description="Unique identifier for the commander")
    commander: str = Field(..., min_length=1, max_length=100, description="Commander name")


class CreateCommander(BaseModel):
    commander: str = Field(..., min_length=1, max_length=100, description="Commander name")


class UpdateCommander(BaseModel):    
    commander: Optional[str] = Field(None, min_length=1, max_length=100, description="Commander name")

class SelectAllCommander(BaseModel):
    pag: Optional[int] = Field(None,description="Offset")
    limit: Optional[int] = Field(None,description="Limit")
    commander: Optional[str] = Field(None, min_length=1, max_length=100, description="Commander name")
