import copy, mwparserfromhell, pypandoc
from datetime import datetime

from bson import ObjectId

from openapi_server.apis.v2_editors_api_base import BaseV2EditorsApi
from openapi_server.impl.utils.api_calls import translate_body_to_lan, translate_text_to_lan, delete_article_ratings, \
    check_if_tag_exists
from openapi_server.impl.utils.functions import mongodb, article_version_to_simplified_article_version, \
    parse_title_to_title_dict, get_total_number_of_documents
from openapi_server.models.models_v2.article_v2 import ArticleV2
from openapi_server.models.models_v2.article_version_v2 import ArticleVersionV2
from openapi_server.models.models_v2.new_article_v2 import NewArticleV2
from openapi_server.models.models_v2.new_article_version_v2 import NewArticleVersionV2


async def _create_article_tranlation(
        new_lan: str,
        title: str,
        og_body: str,
        article_version_id: str,
        translate: bool
) -> None:
    body_translated = copy.deepcopy(og_body)

    body_translated = mwparserfromhell.parse(body_translated)
    body_translated = pypandoc.convert_text(body_translated, to='html', format='mediawiki')

    if translate:
        body_translated = await translate_body_to_lan(body_translated, new_lan)

    article_translation = {
        "lan": new_lan,
        "title": title,
        "body": body_translated,
        "article_version_id": ObjectId(article_version_id),
    }

    await mongodb["article_translation"].insert_one(article_translation)


async def _delete_article_translation(
        article_version_id: str
) -> None:
    await mongodb["article_translation"].delete_many({"article_version_id": ObjectId(article_version_id)})


class EditorsArticleAPIV2(BaseV2EditorsApi):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def create_article_v2(
        self,
        new_article_v2: NewArticleV2,
    ) -> ArticleV2:

        #   Loads the two jsons
        new_article_json = new_article_v2.to_dict()
        new_article_version_json = new_article_v2.to_dict()

        # Checks if the wiki exists (COMMENTED UNTIL IT IS LAUNCHED)
        # if not await check_if_wiki_exists(new_article_json["wiki_id"]):
        #     raise Exception("Wiki does not exist")
        # for tag in new_article_json["tags"]:
        #     if not check_if_tag_exists(tag["id"]):
        #         raise Exception("Tag does not exist")

        if new_article_json["translate_title"]:
            title = new_article_json.pop("title")
            new_article_json["title"]={
                "en": await translate_text_to_lan(title, "en"),
                "es" : await translate_text_to_lan(title, "es"),
                "fr" : await translate_text_to_lan(title, "fr")
            }
        else:
            parse_title_to_title_dict(new_article_json)

        #   Deletes the body key from the article json
        new_article_json.pop("body", None)

        #   Changes the id type and inserts other attributes
        new_article_json["wiki_id"] = ObjectId(new_article_json["wiki_id"])
        new_article_json["author"]["_id"] = ObjectId(new_article_json["author"].pop("id"))

        for tag in new_article_json["tags"]:
            tag["_id"] = ObjectId(tag.pop("id"))

        new_article_json["creation_date"] = datetime.now()
        new_article_json["rating"] = 0
        new_article_json["versions"] = []

        #   MongoDB query
        article_result = await mongodb["article"].insert_one(new_article_json)
        print(article_result)

        #   Deletes the wiki_id from the articleVersion json
        new_article_version_json.pop("wiki_id", None)

        #   Waits for the ArticleVersion object
        article_version = await (
            self.create_article_version_v2(
                str(article_result.inserted_id),
                NewArticleVersionV2.from_dict(new_article_version_json)
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

        return ArticleV2.from_dict(new_article_json)


    async def create_article_version_v2(
        self,
        id: str,
        new_article_version_v2: NewArticleVersionV2,
    ) -> ArticleVersionV2:
        #   Loads the ArticleVersion json
        new_article_version_json = new_article_version_v2.to_dict()

        if new_article_version_json["translate_title"]:
            title = new_article_version_json.pop("title")
            new_article_version_json["title"] = {
                "en": await translate_text_to_lan(title, "en"),
                "es": await translate_text_to_lan(title, "es"),
                "fr": await translate_text_to_lan(title, "fr")
            }
        else:
            parse_title_to_title_dict(new_article_version_json)

        #   Changes the id types in order to insert the document
        new_article_version_json["article_id"] = ObjectId(id)
        new_article_version_json["author"]["_id"] = ObjectId(new_article_version_json["author"].pop("id"))
        new_article_version_json["modification_date"] = datetime.now()
        for tag in new_article_version_json["tags"]:
            tag["_id"] = ObjectId(tag.pop("id"))

        article_tags = copy.deepcopy(new_article_version_json["tags"])

        #   MongoDB query
        article_version_result = await mongodb["article_version"].insert_one(new_article_version_json)

        #   Generate translations
        await _create_article_tranlation(new_article_version_json["lan"],new_article_version_json["title"],
                                         new_article_version_json["body"], article_version_result.inserted_id, False)

        if new_article_version_json["lan"] != "es":
            await _create_article_tranlation("es", new_article_version_json["title"],
                                             new_article_version_json["body"], article_version_result.inserted_id, True)
        if new_article_version_json["lan"] != "en":
            await _create_article_tranlation("en", new_article_version_json["title"],
                                             new_article_version_json["body"], article_version_result.inserted_id, True)
        if new_article_version_json["lan"] != "fr":
            await _create_article_tranlation("fr", new_article_version_json["title"],
                                             new_article_version_json["body"], article_version_result.inserted_id, True)

        #   Undo the changes to id in order to return the ArticleVersion object
        new_article_version_json["id"] = str(article_version_result.inserted_id)
        new_article_version_json["article_id"] = id
        new_article_version_json["author"]["id"] = str(new_article_version_json["author"].pop("_id"))
        for tag in new_article_version_json["tags"]:
            tag["id"] = str(tag.pop("_id"))

        #   Generates a simplified article version
        simplified_article_version_dict = article_version_to_simplified_article_version(
            copy.deepcopy(new_article_version_json))

        #   Add the simplified version to the Article document
        simplified_article_version_dict["_id"] = ObjectId(simplified_article_version_dict.pop("id"))
        simplified_article_version_dict["author"]["_id"] = (
            ObjectId(simplified_article_version_dict["author"].pop("id")))

        # MongoDB query
        await mongodb["article"].update_one(
            {"_id": ObjectId(id)},
            {"$push": {"versions": simplified_article_version_dict},
             "$set": {"title": new_article_version_json["title"],
                      "tags": article_tags}},
        )

        #   Generates the returning ArticleVersion value
        article_version = ArticleVersionV2.from_dict(new_article_version_json)

        return article_version

    async def delete_article_by_idv2(
        self,
        id: str,
    ) -> None:
        article_result = await mongodb["article"].find_one({"_id": ObjectId(id)})
        if article_result is None:
            raise Exception("Article Not Found")

        for version in article_result["versions"]:
            await self.delete_article_version_by_id_v2(str(version["_id"]))

        #   Commented until it's launched
        # await delete_article_comments(id)
        # await delete_article_ratings(id)

        await mongodb["article"].delete_one({"_id": ObjectId(id)})

    async def delete_article_version_by_id_v2(
        self,
        id: str,
    ) -> None:
        result = await mongodb["article_version"].delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise Exception("Article Not Found")

        await _delete_article_translation(id)

    async def restore_article_version_v2(
        self,
        article_id: str,
        version_id: str,
    ) -> None:
        """Restore an older ArticleVersion of an Article."""
        restored_version = await mongodb["article_version"].find_one({"_id": ObjectId(version_id)})
        article = await mongodb["article"].find_one({"_id": ObjectId(article_id)},
                                                    {"versions._id": 1, "versions.modification_date": 1})

        if restored_version is None:
            raise Exception("ArticleVersion Not Found")
        if article is None:
            raise Exception("Article Not Found")

        version_ids_to_delete = [
            version["_id"] for version in article["versions"] if
            version["modification_date"] > restored_version["modification_date"]
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