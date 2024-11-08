from openapi_server.models.tag_id_list import TagIDList
from src.openapi_server.apis.editors_api_base import BaseEditorsApi
class EditorsManager(BaseEditorsApi):
    async def assign_tags(
        self,
        id: str,
        tag_id_list: TagIDList,
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article."""
        ...


    async def unassign_tags(
        self,
        id: str,
        ids: list[str],
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        ...