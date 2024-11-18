import copy
from datetime import datetime, date

from bson import ObjectId

from openapi_server.apis.v1_editors_api_base import BaseV1EditorsApi
from openapi_server.impl.utils.api_calls import delete_article_comments, check_if_wiki_exists
from openapi_server.impl.utils.functions import article_version_to_simplified_article_version, \
    parse_title_to_title_dict, get_original_article_title, get_original_article_version_title, mongodb, \
    get_original_tags
from openapi_server.models.models_v1.article_v1 import ArticleV1
from openapi_server.models.models_v1.article_version_v1 import ArticleVersionV1
from openapi_server.models.models_v1.new_article_v1 import NewArticleV1
from openapi_server.models.models_v1.new_article_version_v1 import NewArticleVersionV1
from openapi_server.models.models_v1.simplified_article_version_v1 import SimplifiedArticleVersionV1

today = date.today()

class EditorArticleAPIV1(BaseV1EditorsApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def create_article_v1(
            self,
            new_article: NewArticleV1,
    ) -> ArticleV1:

        #   Loads the two jsons
        new_article_json = new_article.to_dict()
        new_article_version_json = new_article.to_dict()

        #   Deletes the body key from the article json
        new_article_json.pop("body", None)

        parse_title_to_title_dict(new_article_json)

        # TODO  Checks if the wiki exists (COMMENTED UNTIL IT IS LAUNCHED)
        # if not await check_if_wiki_exists(new_article_json["wiki_id"]):
        #     raise Exception("Wiki does not exist")

        #   Changes the id type and inserts other attributes
        new_article_json["wiki_id"] = ObjectId(new_article_json["wiki_id"])
        new_article_json["author"]["_id"] = ObjectId(new_article_json["author"].pop("id"))
        new_article_json["author"]["image"] = "default_image_url"
        for tag in new_article_json["tags"]:
            tag["_id"] = ObjectId(tag.pop("id"))
            tag["tag"] = {
                "en" : tag["tag"],
                "es" : tag["tag"],
                "fr" : tag["tag"]
            }

        new_article_json["creation_date"] = datetime.now()
        new_article_json["rating"] = 0
        new_article_json["versions"] = []

        #   MongoDB query
        article_result = await mongodb["article"].insert_one(new_article_json)

        #   Deletes the wiki_id from the articleVersion json
        new_article_version_json.pop("wiki_id", None)

        #   Waits for the ArticleVersion object
        article_version = await (
            self.create_article_version_v1(
                str(article_result.inserted_id),
                NewArticleVersionV1.from_dict(new_article_version_json)
            )
        )
        #   Adds the SimplifiedArticleVersion to the returning JSON
        simplified_article_version_dict = article_version_to_simplified_article_version(article_version)
        new_article_json["versions"].append(simplified_article_version_dict)

        #   Undo the previous changes to ids in order to return the Article created
        new_article_json["wiki_id"] = str(new_article_json["wiki_id"])
        new_article_json["author"]["id"] = str(new_article_json["author"].pop("_id"))
        for tag in new_article_json["tags"]:
            tag["id"] = str(tag.pop("_id"))

        new_article_json["id"] = str(article_result.inserted_id)

        get_original_article_title(new_article_json)
        get_original_tags(new_article_json)

        return ArticleV1.from_dict(new_article_json)

    async def create_article_version_v1(
            self,
            id: str,
            new_article_version: NewArticleVersionV1,
    ) -> ArticleVersionV1:

        #   Loads the ArticleVersion json
        new_article_version_json = new_article_version.to_dict()

        #   Sets the title to dict
        parse_title_to_title_dict(new_article_version_json)

        #   Changes the id types in order to insert the document
        new_article_version_json["article_id"] = ObjectId(id)
        new_article_version_json["author"]["_id"] = ObjectId(new_article_version_json["author"].pop("id"))
        new_article_version_json["author"]["image"] = "default_image_url"
        new_article_version_json["modification_date"] = datetime.now()
        for tag in new_article_version_json["tags"]:
            tag["_id"] = ObjectId(tag.pop("id"))
            tag["tag"] = {
                "en": tag["tag"],
                "es": tag["tag"],
                "fr": tag["tag"]
            }

        article_tags = copy.deepcopy(new_article_version_json["tags"])

        #   MongoDB query
        article_version_result = await mongodb["article_version"].insert_one(new_article_version_json)

        #   Undo the changes to id in order to return the ArticleVersion object
        new_article_version_json["id"] = str(article_version_result.inserted_id)
        new_article_version_json["article_id"] = id
        new_article_version_json["author"]["id"] = str(new_article_version_json["author"].pop("_id"))
        for tag in new_article_version_json["tags"]:
            tag["id"] = str(tag.pop("_id"))

        #   Generates a simplified article version
        simplified_article_version_dict = article_version_to_simplified_article_version(copy.deepcopy(new_article_version_json))

        #   Add the simplified version to the Article document
        simplified_article_version_dict["_id"] = ObjectId(simplified_article_version_dict.pop("id"))
        simplified_article_version_dict["author"]["_id"] = (
            ObjectId(simplified_article_version_dict["author"].pop("id")))

        print(article_tags)
        # MongoDB query
        await mongodb["article"].update_one(
            {"_id": ObjectId(id)},
            {"$push": {"versions": simplified_article_version_dict},
             "$set": {"title": new_article_version_json["title"],
                      "tags": article_tags}},
        )



        get_original_article_version_title(new_article_version_json)
        get_original_tags(new_article_version_json)
        #   Generates the returning ArticleVersion value
        article_version = ArticleVersionV1.from_dict(new_article_version_json)

        return article_version

    async def delete_article_by_idv1(
        self,
        id: str,
    ) -> None:

        article_result = await mongodb["article"].find_one({"_id": ObjectId(id)})
        if article_result is None:
            raise Exception("Article Not Found")

        for version in article_result["versions"]:
            await self.delete_article_version_by_id_v1(str(version["_id"]))

        #   Commented until it's launched
        # await delete_article_comments(id)
        #   TODO await delete_article_ratings()

        await mongodb["article"].delete_one({"_id": ObjectId(id)})

    async def delete_article_version_by_id_v1(
        self,
        id: str,
    ) -> None:
        result = await mongodb["article_version"].delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise Exception("Article Not Found")

    async def restore_article_version_v1(
        self,
        article_id: str,
        version_id: str,
    ) -> None:
        """Restore an older ArticleVersion of an Article."""
        restored_version = await mongodb["article_version"].find_one({"_id": ObjectId(version_id)})
        article = await mongodb["article"].find_one({"_id": ObjectId(article_id)}, {"versions._id": 1, "versions.modification_date": 1})

        if restored_version is None:
            raise Exception("ArticleVersion Not Found")
        if article is None:
            raise Exception("Article Not Found")

        version_ids_to_delete = [
            version["_id"] for version in article["versions"] if version["modification_date"] > restored_version["modification_date"]
        ]

        result = await mongodb["article"].update_one(
            {"_id": ObjectId(article_id)},
            {"$pull": {"versions": {"_id": {"$in": version_ids_to_delete}}},
             "$set": {"title": restored_version["title"],
                      "tags": restored_version["tags"]}},
        )

        if version_ids_to_delete:
            await mongodb["article_version"].delete_many({"_id": {"$in": version_ids_to_delete}})

        return None