from models.base import BaseModel
from typing import List, Optional, Literal

class Component(BaseModel):
    id: str
    unit: Literal["gr", "ml", "unidad"]
    quantity: float
    
class Ingredient(BaseModel):
    id: str
    unit: Literal["gr", "ml", "unidad"]
    quantity: float

class Option(BaseModel):
    id: str
    display_name: str
    unit: Literal["gr", "ml", "unidad"]
    quantity: float
    price: float


class FinalArticlesInput(BaseModel):
    category_id : Optional[str] = None
    kitchen : str
    name : str
    description : str
    price : float
    is_prepared : bool
    options : Optional[List[Option]] = None
    components: Optional[List[Component]] = None
    ingredients: Optional[List[Ingredient]] = None
    stock_controlled : bool

class FinalArticlesUpdateInput(BaseModel):
    category_id : Optional[str] = None
    kitchen : Optional[str] = None
    name : Optional[str] = None
    description : Optional[str] = None
    price : Optional[float] = None
    is_prepared : Optional[bool] = None
    options : Optional[List[Option]] = None
    components: Optional[List[Component]] = None
    ingredients: Optional[List[Ingredient]] = None
    stock_controlled : Optional[bool] = None
    
class FinalArticlesInputComplet(FinalArticlesInput):
    restaurant_id : str