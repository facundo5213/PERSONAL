from typing import TypeVar, Generic, Type
from pymongo.client_session import ClientSession

from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from pydantic import BaseModel

from utils.presentation.errors import NotFoundException

DbModel = TypeVar('DbModel', bound=BaseModel)


class BaseRepository(Generic[DbModel]):
    _entity_model: Type[DbModel]

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection: AsyncIOMotorCollection = db.get_collection(self._entity_model._collection_name.default)

    async def get(self, document_id: str, raise_exception=True) -> DbModel:
        instance = await self.collection.find_one({"_id": document_id})
        if not instance and raise_exception:
            raise NotFoundException(f" Document {document_id} not found in "
                                    f"{self._entity_model._collection_name.default} collection.")
        return self._entity_model(**instance)

    async def get_active_by_id(self, document_id: str, raise_exception=True) -> DbModel:
        instance = await self.collection.find_one({"_id": document_id, "is_deleted": False})
        if not instance and raise_exception:
            raise NotFoundException(f" Document {document_id} not found in "
                                    f"{self._entity_model._collection_name.default} collection.")
        return self._entity_model(**instance)

    async def get_all_actives(self, raise_exception=True) -> list[DbModel]:
        instances = await self.collection.find({"is_deleted": False}).to_list(None)
        if not instances and raise_exception:
            raise NotFoundException(f" Documents not found in "
                                    f"{self._entity_model._collection_name.default} collection.")
        return [self._entity_model(**instance) for instance in instances]

    async def create(self, data: BaseModel, session: ClientSession = None) -> DbModel:
        validated_data = self._entity_model.model_validate(data.model_dump()).model_dump(mode="json")
        validated_data["_id"] = validated_data.pop("id")
        await self.collection.insert_one(validated_data, session=session)
        return self._entity_model(**validated_data)

    async def update(self, document_id: str, data: BaseModel) -> DbModel:
        validated_data = self._entity_model.model_validate(data).model_dump(mode="json")
        if "id" in validated_data:
            validated_data.pop("id")
        await self.collection.find_one_and_update(
            {"_id": document_id},
            {"$set": validated_data},
        )
        return self._entity_model(**validated_data)

    async def patch(self, document_id: str, patch_input: BaseModel) -> DbModel:
        instance = await self.get_active_by_id(document_id)
        update_data = patch_input.model_dump(exclude_unset=True)
        updated_instance = instance.model_copy(update=update_data)
        return await self.update(instance.id, updated_instance)

    async def delete(self, document_id: str) -> None:
        await self.collection.delete_one({"_id": document_id})

    async def soft_delete(self, document_id: str) -> None:
        await self.collection.find_one_and_update(
            {"_id": document_id},
            {"$set": {"is_deleted": True}}
        )
        instance = await self.collection.find_one({"_id": document_id})
        return self._entity_model(**instance)
