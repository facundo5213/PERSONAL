from models.base import Base
from typing import List, Optional, Literal
from datetime import datetime


class OrdersModel(Base):
    _collection_name = "orders"

    #user_id: PyObjectId
    restaurant_id: str
    table_id: Optional[str] = None
    menu_items: list[dict] = []
    """ Ejemplo: [  {   "final_article_id": "item1",
                        "options": ["option_id"],
                        "quantity": 2,
                        "status": "pending",
                        "item_number": 1,
                        "price": 10.00
                    },
                    {   ... }]
    """
    menu_groups: list[dict] = [] 
    """Ejemplo: [   {"menu_id": "str", "items": [{menu_items}], "price": 20.00
                    }, {...}]
    """
    assigned_employee: str
    closed_order_at: Optional[datetime] = None
    comments: Optional[str] = None
    amount: float
    status: Literal["open", "cancelled", "closed"] = "open"
    order_type: Literal["dine_in", "takeaway", "delivery"] = "dine_in"

