from openapi_server.apis.v2_apis.v2_admins_api_base import BaseV2AdminsApi
from openapi_server.impl.utils import TAGS_URL,WIKIS_URL
from openapi_server.impl.utils import forward_request
from openapi_server.models.new_tag import NewTag
from openapi_server.models.new_wiki import NewWiki
from openapi_server.models.tag import Tag
from openapi_server.models.wiki import Wiki


class APIGatewayEditorsV2(BaseV2AdminsApi):

    def __init__(self):
        super().__init__()

    async def create_wiki(
        self,
        new_wiki: NewWiki,
    ) -> Wiki:
        """Create a new Wiki"""
        return await forward_request(method="POST", url=f"{WIKIS_URL}/v2/wikis", json=new_wiki.to_dict())


    async def delete_tag(
        self,
        id: str,
    ) -> None:
        """Delete a wiki tag."""
        return await forward_request(method="DELETE", url=f"{TAGS_URL}/v2/tags/{id}")


    async def post_wiki_tag(
        self,
        id: str,
        new_tag: NewTag,
    ) -> Tag:
        """Create a new tag in a given wiki."""
        return await forward_request(method="POST", url=f"{TAGS_URL}/v2/tags/wikis/{id}", json=new_tag.to_dict())


    async def remove_wiki(
        self,
        id_name: str,
    ) -> None:
        """Remove Wiki with the matching ID."""
        return await forward_request(method="DELETE", url=f"{WIKIS_URL}/v2/wikis/{id_name}")


    async def update_wiki(
        self,
        id_name: str,
        new_wiki: NewWiki,
    ) -> Wiki:
        """Update Wiki with wiki the matching ID"""
        return await forward_request(method="Put", url=f"{WIKIS_URL}/v2/wikis/{id_name}", json=new_wiki.to_dict())