from datetime import datetime, timezone
from uuid import uuid4

from pydantic import Field, BaseModel, ConfigDict


class Base(BaseModel):
    _collection_name: str
    model_config = ConfigDict(populate_by_name=True, extra="ignore", use_enum_values=True)
    
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_deleted: bool = False


