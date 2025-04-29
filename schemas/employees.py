from pydantic import BaseModel, EmailStr
from typing import List


class EmployeeInput(BaseModel):
    _collection_name = "employee"

    identifier: int  
    name: str
    role: str
    comments: str
    phone: str
    address: str
    email: EmailStr
    emergency_contact: int
    work_schedule: str
    assigned_tables: List[dict] = []

    
class EmployeeInputComplete(BaseModel):
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


class EmployeeLogin(BaseModel):
    _collection_name = "employee"

    identifier: int  
