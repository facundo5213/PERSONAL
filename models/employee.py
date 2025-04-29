from models.base import Base
from pydantic import EmailStr, Field, BaseModel
from typing import List, Optional


class EmployeeModel(Base):
    _collection_name = "employee"

    identifier: int  
    name: str
    role: str
    comments: str
    phone: str
    address: str
    email: EmailStr
    restaurant_id: str
    emergency_contact: int
    work_schedule: str
    assigned_tables: List[dict] = []

class EmployeeIdResponse(BaseModel):
    employee_id : str


