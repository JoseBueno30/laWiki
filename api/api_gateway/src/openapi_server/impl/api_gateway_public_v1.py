from typing import List

from openapi_server.apis.v1_public_api_base import BaseV1PublicApi
from openapi_server.impl.utils import ARTICLES_URL,COMMENTS_URL,RATINGS_URL,TAGS_URL,WIKIS_URL
from openapi_server.models.article import Article
from openapi_server.models.article_list import ArticleList
from openapi_server.models.article_version import ArticleVersion
from openapi_server.models.article_version_body import ArticleVersionBody
from openapi_server.models.article_version_list import ArticleVersionList
from openapi_server.models.average_rating import AverageRating
from openapi_server.models.comment import Comment
from openapi_server.models.comment_list_response import CommentListResponse
from openapi_server.models.new_comment import NewComment
from openapi_server.models.new_rating import NewRating
from openapi_server.models.rating import Rating
from openapi_server.models.tag import Tag
from openapi_server.models.tag_list import TagList
from openapi_server.models.wiki import Wiki
from openapi_server.models.wiki_list import WikiList

from openapi_server.impl.utils import forward_request

class APIGatewayPublicV1(BaseV1PublicApi):

    async def delete_comment(
        self,
        comment_id: str,
    ) -> None:
        """Deletes an article&#39;s comment"""
        return await forward_request("DELETE", f"{COMMENTS_URL}/comments/{comment_id}")


    async def delete_rating(
        self,
        id: str,
    ) -> None:
        """Delete the rating associated with the selected ID"""
        return await forward_request("DELETE", f"{RATINGS_URL}/ratings/{id}")


    async def edit_article_rating(
        self,
        id: str,
        new_rating: NewRating,
    ) -> Rating:
        """Update the value of an already existing Rating"""
        return await forward_request(method="PUT",url=f"{RATINGS_URL}/ratings/articles/{id}",json=new_rating.to_dict())


    async def get_article_average_rating(
        self,
        id: str,
    ) -> AverageRating:
        """Get data about the average rating of the article"""
        return await forward_request(method="GET",url=f"{RATINGS_URL}/ratings/articles/{id}/average")


    async def get_article_by_author(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleList:
        """Get a list of Articles given an author&#39;s ID.  """
        query_params = {"offset": offset, "limit":limit, "order":order}
        response = await forward_request(method="GET",url=f"{ARTICLES_URL}/v2/articles/author/{id}", query_params=query_params)
        response["next"] = response["next"].replace("/v2/", "/v1/") if response["next"] else None
        response["previous"] = response["previous"].replace("/v2/", "/v1/") if response["previous"] else None

        return response


    async def get_article_by_id(
        self,
        id: str,
    ) -> Article:
        """Get an Article identified by it&#39;s unique ID"""
        return await forward_request(method="GET",url=f"{ARTICLES_URL}/v2/articles/{id}")


    async def get_article_by_name(
        self,
        name: str,
        wiki: str,
        lan: str,
    ) -> ArticleVersion:
        """Get the most recent ArticleVersion the Article with the given name from the specified Wiki."""
        query_params={"wiki":wiki, "lan":lan}
        return await forward_request(method="GET",url=f"{ARTICLES_URL}/v2/articles/versions/by-name{name}", query_params=query_params)


    async def get_article_comments(
        self,
        article_id: str,
        order: str,
        limit: int,
        offset: int,
        creation_date: str,
    ) -> CommentListResponse:
        """Retrieves all comments from an articles"""
        query_params = {"order": order, "limit": limit, "offset":offset, "creation_date":creation_date}
        response = await forward_request(method="GET",url=f"{COMMENTS_URL}/comments/articles/{article_id}",query_params=query_params)
        response["next"] = "/v1" + response["next"] if response["next"] else None
        response["previous"] = "/v1" + response["previous"] if response["previous"] else None

        return response

    async def get_article_from_specific_wiki(
        self,
        wiki_name: str,
        article_name: str,
        lan: str,
    ) -> ArticleVersion:
        """Get the most recent ArticleVersion the Article with the given name from the Wiki with the given name. Endpoint thought to access articles when only the names of the Wiki and Article are known, with a textual URL for example."""
        query_params = {"lan": lan}
        wiki = await forward_request(method="GET",url=f"{WIKIS_URL}/v2/wikis/{wiki_name}",query_params=query_params)
        query_params = {"lan": lan, "wiki_id":wiki["id"]}
        return await forward_request(method="GET", url=f"{ARTICLES_URL}/v2/articles/versions/by-name/{article_name}", query_params=query_params)


    async def get_article_version_body_by_id(
        self,
        id: str,
        parsed: bool,
        lan: str,
    ) -> ArticleVersionBody:
        query_params = {"parsed": parsed, "lan": lan}
        return await forward_request(method="GET", url=f"{ARTICLES_URL}/v2/articles/versions/{id}/body",query_params=query_params)


    async def get_article_version_by_id(
        self,
        id: str,
        lan: str,
    ) -> ArticleVersion:
        """Get an ArticleVersion identified by it&#39;s unique ID"""
        query_params = {"lan": lan}
        return await forward_request(method="GET", url=f"{ARTICLES_URL}/v2/articles/versions/{id}",query_params=query_params)


    async def get_article_version_list_by_article_id(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleVersionList:
        """Get a list of ArticleVersions of a given Article. Results can be sorted by creation date adn support pagination."""
        query_params = {"offset": offset, "limit":limit, "order":order}
        return await forward_request(method="GET", url=f"{ARTICLES_URL}/v2/articles/{id}/versions",query_params=query_params)


    async def get_articles_commented_by_user(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleList:
        """Get a list of the Articles commented by a given user."""
        query_params = {"offset": offset, "limit":limit, "order":order}
        response = await forward_request(method="GET", url=f"{ARTICLES_URL}/v2/articles/commented_by/{id}",query_params=query_params)
        response["next"] = response["next"].replace("/v2/", "/v1/") if response["next"] else None
        response["previous"] = response["previous"].replace("/v2/", "/v1/") if response["previous"] else None

        return response


    async def get_articles_tags(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagList:
        """Retrieves all the tags from an article."""
        query_params = {"offset": offset, "limit": limit}
        response = await forward_request(method="GET", url=f"{TAGS_URL}/v2/tags/articles/{id}",query_params=query_params)
        response["next"] = response["next"].replace("/v2/", "/v1/") if response["next"] else None
        response["previous"] = response["previous"].replace("/v2/", "/v1/") if response["previous"] else None

        return response

    async def get_rating(
        self,
        id: str,
    ) -> Rating:
        """Get the Rating with the provided ID"""
        return await forward_request(method="GET", url=f"{RATINGS_URL}/ratings/{id}")


    async def get_ratings_bu_user_on_article(
        self,
        articleId: str,
        userId: str,
    ) -> Rating:
        return await forward_request(method="GET", url=f"{RATINGS_URL}/ratings/article/{articleId}/users/{userId}")

    async def get_tag(
        self,
        id: str,
    ) -> Tag:
        """Get a tag by ID. """
        return await forward_request(method="GET", url=f"{TAGS_URL}/v2/tags/{id}")

    async def get_users_comments(
        self,
        user_id: str,
        article_id: str,
        order: str,
        limit: int,
        offset: int,
        creation_date: str,
    ) -> CommentListResponse:
        """Retrieves all comments from an user"""
        query_params = {"article_id":article_id, "order":order, "limit":limit, "offset":offset, "creation_date":creation_date}
        response = await forward_request(method="GET", url=f"{COMMENTS_URL}/comments/users/{user_id}", query_params=query_params)
        response["next"] = "/v1" + response["next"] if response["next"] else None
        response["previous"] = "/v1" + response["previous"] if response["previous"] else None

        return response


    async def get_wiki(
        self,
        id_name: str,
        lang: str,
    ) -> Wiki:
        """Get Wiki with the matching ID."""
        query_params = {"lang": lang}
        return await forward_request(method="GET", url=f"{WIKIS_URL}/v2/wikis/{id_name}", query_params=query_params)


    async def get_wiki_tags(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagList:
        """Retrieve all the tags from a wiki."""
        query_params = {"limit": limit, "offset": offset}
        response = await forward_request(method="GET", url=f"{TAGS_URL}/v2/tags/wikis/{id}", query_params=query_params)
        response["next"] = response["next"].replace("/v2/", "/v1/") if response["next"] else None
        response["previous"] = response["previous"].replace("/v2/", "/v1/") if response["previous"] else None

        return response

    async def post_comment(
        self,
        article_id: str,
        new_comment: NewComment,
    ) -> Comment:
        """Posts a new comment in an article"""
        return await forward_request(method="POST", url=f"{COMMENTS_URL}/comments/articles/{article_id}", json=new_comment.to_dict())


    async def rate_article(
        self,
        id: str,
        new_rating: NewRating,
    ) -> Rating:
        """Create a rating for a given Article"""
        return await forward_request(method="POST", url=f"{RATINGS_URL}/ratings/articles/{id}", json=new_rating.to_dict())


    async def search_articles(
        self,
        wiki_id: str,
        name: str,
        tags: List[str],
        offset: int,
        limit: int,
        order: str,
        creation_date: str,
        author_name: str,
        editor_name: str,
        lan: str,
    ) -> ArticleList:
        """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        query_params = {"wiki_id":wiki_id, "name": name, "tags":tags, "offset": offset, "limit": limit, "order": order, "creation_date": creation_date,"author_name": author_name, "editor_name":editor_name, "lan": lan}
        response = await forward_request(method="GET", url=f"{ARTICLES_URL}/v2/articles", query_params=query_params)
        response["next"] = response["next"].replace("/v2/", "/v1/") if response["next"] else None
        response["previous"] = response["previous"].replace("/v2/", "/v1/") if response["previous"] else None

        return response


    async def search_wikis(
        self,
        name: str,
        limit: int,
        offset: int,
        order: str,
        creation_date: str,
        author_name: str,
        lang: str,
    ) -> WikiList:
        """Get a list of Wikis that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        query_params = {"name":name, "offset": offset, "limit": limit, "order":order, "creation_date":creation_date, "author_name":author_name, "lang":lang}
        response = await forward_request(method="GET", url=f"{WIKIS_URL}/v2/wikis", query_params=query_params)
        response["next"] = response["next"].replace("/v2/", "/v1/") if response["next"] else None
        response["previous"] = response["previous"].replace("/v2/", "/v1/") if response["previous"] else None

        return response