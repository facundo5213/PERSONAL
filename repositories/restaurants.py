from models.restaurants import RestaurantsModel
from repositories.crud import BaseRepository


class RestaurantRepository(BaseRepository[RestaurantsModel]):
    _entity_model = RestaurantsModel
