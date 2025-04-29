from models.base import Base
from typing import List, Optional

class VendorModel(Base):
    _collection_name = "Vendor"

    cuit: str
    name: str
    company_name: str
    phone: str
    email: str
    adress: str