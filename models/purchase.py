from models.base import Base
from typing import List, Optional

class PurchaseModel(Base):
    _collection_name = "purchase"

    vendor_id: str
    receipt_id: str
    stock_id: str
    quantity: str 
    unit: float
    unit_price: float
    discount: float