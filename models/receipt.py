from models.base import Base
from typing import List, Optional

class ReceiptModel(Base):
    _collection_name = "receipt"


    vendor_id: str
    stock_id: List[dict] = []
    type: List[dict] = []
    date: str
    due_date: str
    vat: float
    total_due: float
    

