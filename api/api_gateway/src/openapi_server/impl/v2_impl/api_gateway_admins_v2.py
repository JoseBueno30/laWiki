from openapi_server.apis.v2_apis.v2_admins_api_base import BaseV2AdminsApi
from openapi_server.impl.utils import TAGS_API_URL,WIKIS_API_URL
from openapi_server.impl.utils import forward_request
from openapi_server.models.extra_models import TokenModel
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
        decoded_token: TokenModel,
    ) -> Wiki:
        """Create a new Wiki"""
        headers_params = {
            "user-id": decoded_token.user_info["id"],
            "admin": decoded_token.user_info["admin"]
        }
        return await forward_request(method="POST", url=f"{WIKIS_API_URL}/v3/wikis", json=new_wiki.to_dict(), headers_params=headers_params)


    async def delete_tag(
        self,
        id: str,
        decoded_token: TokenModel,
    ) -> None:
        """Delete a wiki tag."""
        headers_params = {
            "user-id": decoded_token.user_info["id"],
            "admin": decoded_token.user_info["admin"]
        }
        return await forward_request(method="DELETE", url=f"{TAGS_API_URL}/v3/tags/{id}", headers_params=headers_params)


    async def post_wiki_tag(
        self,
        id: str,
        new_tag: NewTag,
        decoded_token: TokenModel,
    ) -> Tag:
        """Create a new tag in a given wiki."""
        headers_params = {
            "user-id": decoded_token.user_info["id"],
            "admin": decoded_token.user_info["admin"]
        }
        return await forward_request(method="POST", url=f"{TAGS_API_URL}/v3/tags/wikis/{id}", json=new_tag.to_dict(), headers_params=headers_params)


    async def remove_wiki(
        self,
        id_name: str,
        decoded_token: TokenModel,
    ) -> None:
        """Remove Wiki with the matching ID."""
        headers_params = {
            "user-id": decoded_token.user_info["id"],
            "admin": decoded_token.user_info["admin"]
        }
        return await forward_request(method="DELETE", url=f"{WIKIS_API_URL}/v3/wikis/{id_name}", headers_params=headers_params)


    async def update_wiki(
        self,
        id_name: str,
        new_wiki: NewWiki,
        decoded_token: TokenModel,
    ) -> Wiki:
        """Update Wiki with wiki the matching ID"""
        headers_params = {
            "user-id": decoded_token.user_info["id"],
            "admin": decoded_token.user_info["admin"]
        }
        return await forward_request(method="Put", url=f"{WIKIS_API_URL}/v3/wikis/{id_name}", json=new_wiki.to_dict(), headers_params=headers_params)