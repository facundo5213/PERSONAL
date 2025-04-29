from models.users import UsersModel, UserResponseModel
from repositories.crud import BaseRepository


class UsersRepository(BaseRepository[UsersModel]):
    _entity_model = UsersModel


class UsersRepositoryResponse(BaseRepository[UserResponseModel]):
    _entity_model = UserResponseModel


class UsersRepositoryLogin:
    def __init__(self, db):
        self.collection = db["users"]

    async def get_by_email(self, email: str) -> dict:
        user = await self.collection.find_one({"email": email})
        return user
