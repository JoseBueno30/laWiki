import json
from datetime import datetime, date

from bson import ObjectId

from openapi_server.apis.editors_api import create_article_version
from openapi_server.apis.editors_api_base import BaseEditorsApi
from openapi_server.impl.default_article_api import mongodb
from openapi_server.models.article import Article
from openapi_server.models.article_version import ArticleVersion
from openapi_server.models.new_article import NewArticle
from openapi_server.models.new_article_version import NewArticleVersion
from openapi_server.models.simplified_article_version import SimplifiedArticleVersion

today = date.today()

def article_version_to_simplified_article_version(article_version):
    simplified_article_version = article_version.to_dict()

    #   Deletes the non-necessary attributes
    simplified_article_version.pop("article_id", None)
    simplified_article_version.pop("tags", None)
    simplified_article_version.pop("body", None)

    return SimplifiedArticleVersion.from_dict(simplified_article_version)

class EditorArticleAPI(BaseEditorsApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def create_article(
            self,
            new_article: NewArticle,
    ) -> Article:

        #   Loads the two jsons
        new_article_json = new_article.to_dict()
        new_article_version_json = new_article.to_dict()

        #   Deletes the body key from the article json
        new_article_json.pop("body", None)

        #   Changes the id type and inserts other attributes
        new_article_json["wiki_id"] = ObjectId(new_article_json["wiki_id"])
        new_article_json["author"]["_id"] = ObjectId(new_article_json["author"].pop("id"))
        for tag in new_article_json["tags"]:
            tag["_id"] = ObjectId(tag.pop("id"))

        new_article_json["creation_date"] = datetime(today.year, today.month, today.day)
        new_article_json["rating"] = 0
        new_article_json["versions"] = []

        #   MongoDB query
        article_result = await mongodb["article"].insert_one(new_article_json)

        #   Deletes the wiki_id from the articleVersion json
        new_article_version_json.pop("wiki_id", None)

        #   Waits for the ArticleVersion object
        article_version = await (
            create_article_version(
                str(article_result.inserted_id),
                NewArticleVersion.from_dict(new_article_version_json)
            )
        )

        simplified_article_version = article_version_to_simplified_article_version(article_version)

        #   Add the version to the Article document
        simplified_article_version_dict = simplified_article_version.to_dict()
        simplified_article_version_dict["_id"] = ObjectId(simplified_article_version_dict.pop("id"))
        await mongodb["article"].update_one(
            {"_id": article_result.inserted_id},
            {"$set": {"versions" : [simplified_article_version_dict]}}
        )
        simplified_article_version_dict["id"] = str(simplified_article_version_dict.pop("_id"))
        new_article_json["versions"].append(simplified_article_version_dict)

        #   Undo the previous changes to ids in order to return the Article created
        new_article_json["wiki_id"] = str(new_article_json["wiki_id"])
        new_article_json["author"]["id"] = str(new_article_json["author"].pop("_id"))
        for tag in new_article_json["tags"]:
            tag["id"] = str(tag.pop("_id"))

        new_article_json["id"] = str(article_result.inserted_id)
        return Article.from_dict(new_article_json)

    async def create_article_version(
            self,
            id: str,
            new_article_version: NewArticleVersion,
    ) -> ArticleVersion:

        #   Loads the ArticleVersion json
        new_article_version_json = new_article_version.to_dict()

        #   Changes the id types in order to insert the document
        new_article_version_json["article_id"] = ObjectId(id)
        new_article_version_json["author"]["_id"] = ObjectId(new_article_version_json["author"].pop("id"))
        new_article_version_json["modification_date"] = datetime(today.year, today.month, today.day)
        for tag in new_article_version_json["tags"]:
            tag["_id"] = ObjectId(tag.pop("id"))

        #   MongoDB query
        article_version_result = await mongodb["article_version"].insert_one(new_article_version_json)

        #   Undo the changes to id in order to return the ArticleVersion object
        new_article_version_json["id"] = str(article_version_result.inserted_id)
        new_article_version_json["article_id"] = id
        new_article_version_json["author"]["id"] = str(new_article_version_json["author"].pop("_id"))
        for tag in new_article_version_json["tags"]:
            tag["id"] = str(tag.pop("_id"))

        return ArticleVersion.from_dict(new_article_version_json)
