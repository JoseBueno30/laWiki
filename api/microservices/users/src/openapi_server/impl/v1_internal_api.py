from openapi_server.apis.v1_internal_api_base import BaseV1InternalApi
from openapi_server.models.new_rating import NewRating


class V1InternalAPI(BaseV1InternalApi):

    async def check_user(
        self,
        user_id: str,
    ) -> None:
        """Checks wheter the user email is registered in the application"""
        ...

    async def put_user_rating(
        self,
        user_id: str,
        new_rating: NewRating,
    ) -> None:
        """Update the given user's rating"""
        ...