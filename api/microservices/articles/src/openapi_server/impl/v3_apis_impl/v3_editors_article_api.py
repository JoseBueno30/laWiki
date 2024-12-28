import copy, mwparserfromhell, pypandoc
import json
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
import re

from pydantic.v1 import StrictStr, StrictBool

from openapi_server.apis.v3_editors_api_base import BaseV3EditorsApi
from openapi_server.impl.utils.api_calls import translate_body_to_lan, translate_text_to_lan, delete_article_ratings, \
    check_if_tag_exists, check_if_wiki_exists, delete_article_comments, get_wiki_author, get_user
from openapi_server.impl.utils.functions import mongodb, article_version_to_simplified_article_version, \
    parse_title_to_title_dict, get_total_number_of_documents
from openapi_server.impl.utils.emails_service import send_email
from openapi_server.models.models_v2.article_v2 import ArticleV2
from openapi_server.models.models_v2.article_version_v2 import ArticleVersionV2
from openapi_server.models.models_v2.new_article_v2 import NewArticleV2
from openapi_server.models.models_v2.new_article_version_v2 import NewArticleVersionV2


async def _create_article_translation(
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
        body_translated.replace("<mapview", "<MapView")
        print("LAN: ", new_lan, "\n", body_translated)

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


def _is_valid_name(name):
    # Expresión regular que permite letras con tildes, ñ, números y espacios
    pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9 ]+$'
    return bool(re.match(pattern, name))

class EditorsArticleAPIV3(BaseV3EditorsApi):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def create_article_v3(
        self,
        user_id: StrictStr,
        admin: StrictBool,
        new_article_v2: Optional[NewArticleV2],
    ) -> ArticleV2:
        #   Loads the two jsons
        new_article_json = new_article_v2.to_dict()
        new_article_version_json = new_article_v2.to_dict()

        if user_id != new_article_json["author"]["id"]:
            raise Exception("User ID does not match the author ID")

        if not _is_valid_name(new_article_json["title"]) and ObjectId.is_valid(new_article_json["title"]):
            raise Exception(f"Invalid article title: {new_article_json['title']}")

        if not await check_if_wiki_exists(new_article_json["wiki_id"]):
            raise Exception("Wiki does not exist")
        for tag in new_article_json["tags"]:
            if not check_if_tag_exists(tag["id"]):
                raise Exception("Tag does not exist")

        if new_article_json["translate_title"]:
            title = new_article_json.pop("title")
            new_article_json["title"] = {
                "en": await translate_text_to_lan(title, "en"),
                "es": await translate_text_to_lan(title, "es"),
                "fr": await translate_text_to_lan(title, "fr")
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
            self.create_article_version_v3(
                str(article_result.inserted_id),
                user_id,
                admin,
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

    async def create_article_version_v3(
        self,
        id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
        new_article_version_v2: NewArticleVersionV2,
    ) -> ArticleVersionV2:
        #   Loads the ArticleVersion json
        new_article_version_json = new_article_version_v2.to_dict()

        if user_id != new_article_version_json["author"]["id"]:
            raise Exception("User ID does not match the author ID")
        
        article_result = await mongodb["article"].find_one({"_id": ObjectId(id)})
        article_author = await get_user(article_result["author"]["_id"])
        user = await get_user(user_id)
        
        if not _is_valid_name(new_article_version_json["title"]) and ObjectId.is_valid(
                new_article_version_json["title"]):
            raise Exception(f"Invalid article title: {new_article_version_json['title']}")

        for tag in new_article_version_json["tags"]:
            if not check_if_tag_exists(tag["id"]):
                raise Exception("Tag does not exist")

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
        await _create_article_translation(new_article_version_json["lan"], new_article_version_json["title"],
                                          new_article_version_json["body"], article_version_result.inserted_id, False)

        if new_article_version_json["lan"] != "es":
            await _create_article_translation("es", new_article_version_json["title"],
                                              new_article_version_json["body"], article_version_result.inserted_id,
                                              True)
        if new_article_version_json["lan"] != "en":
            await _create_article_translation("en", new_article_version_json["title"],
                                              new_article_version_json["body"], article_version_result.inserted_id,
                                              True)
        if new_article_version_json["lan"] != "fr":
            await _create_article_translation("fr", new_article_version_json["title"],
                                              new_article_version_json["body"], article_version_result.inserted_id,
                                              True)

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
            {"$push": {"versions": {"$each": [simplified_article_version_dict], "$position": 0}},
             "$set": {"title": new_article_version_json["title"],
                      "tags": article_tags}},
        )

        body_new_article_version = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 0;">
            <div style="background-color: #28a745; color: white; padding: 20px; text-align: center;">
            <h1 style="margin: 0;">A New Version of Your Article Has Been Created!</h1>
            <p style="margin: 10px 0;">Your article has been updated with a new version created by <strong>{user['email']}</strong>.</p>
            </div>
            
            <div style="padding: 20px; background-color: #ffffff;">
            <h2 style="color: #28a745;">Article Details</h2>
            <p><strong>Article Title:</strong> <em>{article_result['title']['en']}</em></p>
            <p><strong>New Version Title:</strong> <em>{new_article_version_json["title"]['en']}</em></p>
            <p><strong>Summary of Changes:</strong> A new version of your article has been created. Please review the latest changes to ensure they align with your expectations.</p>
            </div>
        </body>
        </html>
        """

        send_email(article_author['email'], "A New Version of Your Article Has Been Created!", body_new_article_version)

        #   Generates the returning ArticleVersion value
        article_version = ArticleVersionV2.from_dict(new_article_version_json)

        return article_version

    async def delete_article_by_idv3(
        self,
        id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
    ) -> None:
        article_result = await mongodb["article"].find_one({"_id": ObjectId(id)})
        article_author = await get_user(article_result["author"]["_id"])
        user = await get_user(user_id)

        if not admin and user_id != str(article_result["author"]["_id"]):
            raise Exception("User can't delete this article")

        if article_result is None:
            raise Exception("Article Not Found")

        for version in article_result["versions"]:
            await self.delete_article_version_by_id_v3(str(version["_id"]))

            version_author = await get_user(version["author"]["_id"])
            
            body_version_deletion = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 0;">
                <div style="background-color: #dc3545; color: white; padding: 20px; text-align: center;">
                <h1 style="margin: 0;">Your Article Version Has Been Deleted!</h1>
                <p style="margin: 10px 0;">The user with email <strong>{user['email']}</strong> has deleted one of your article versions.</p>
                </div>
                
                <div style="padding: 20px; background-color: #ffffff;">
                <h2 style="color: #dc3545;">Deletion Details</h2>
                <p><strong>Deleted Article Version:</strong> <em>{version['title']['en']}</em></p>
                </div>
            </body>
            </html>
            """
            if version_author['email'] != article_author['email']:
                send_email(version_author['email'], "Your Article Version Has Been Deleted!", body_version_deletion)

        #   Commented until it's launched
        await delete_article_comments(id)
        await delete_article_ratings(id)

        await mongodb["article"].delete_one({"_id": ObjectId(id)})

        body_deletion_article = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 0;">
            <div style="background-color: #dc3545; color: white; padding: 20px; text-align: center;">
            <h1 style="margin: 0;">Your Article Has Been Deleted!</h1>
            <p style="margin: 10px 0;">The user with email <strong>{user['email']}</strong> has deleted one of your articles.</p>
            </div>
            
            <div style="padding: 20px; background-color: #ffffff;">
            <h2 style="color: #dc3545;">Deletion Details</h2>
            <p><strong>Deleted Article:</strong> <em>{article_result['title']['en']}</em></p>
            </div>
        </body>
        </html>
        """

        send_email(article_author['email'], "Your Article Has Been Deleted!", body_deletion_article)

    async def delete_article_version_by_id_v3(
        self,
        id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
    ) -> None:
        
        article_version = await mongodb["article_version"].find_one({"_id": ObjectId(id)})
        article = await mongodb["article"].find_one({"_id": ObjectId(article_version["article_id"])})
        article_version_author = await get_user(article_version["author"]["_id"])
        article_author = await get_user(article["author"]["_id"])
        user = await get_user(user_id)

        result = await mongodb["article_version"].delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise Exception("Article Not Found")

        await _delete_article_translation(id)
        body_article_version_author = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 0;">
            <div style="background-color: #dc3545; color: white; padding: 20px; text-align: center;">
            <h1 style="margin: 0;">Your Article Version Has Been Deleted!</h1>
            <p style="margin: 10px 0;">The user with email <strong>{user['email']}</strong> has deleted your article version.</p>
            </div>
            
            <div style="padding: 20px; background-color: #ffffff;">
            <h2 style="color: #dc3545;">Deletion Details</h2>
            <p><strong>Deleted Article Version:</strong> <em>{article_version['title']['en']}</em></p>
            </div>
        </body>
        </html>
        """

        body_article_author = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 0;">
            <div style="background-color: #dc3545; color: white; padding: 20px; text-align: center;">
                <h1 style="margin: 0;">A Version of Your Article Has Been Deleted!</h1>
                <p style="margin: 10px 0;">The user with email <strong>{user['email']}</strong> has deleted a version of your article.</p>
            </div>
            
            <div style="padding: 20px; background-color: #ffffff;">
                <h2 style="color: #dc3545;">Deletion Details</h2>
                <p><strong>Article Title:</strong> <em>{article['title']['en']}</em></p>
                <p><strong>Deleted Version Title:</strong> <em>{article_version['title']['en']}</em></p>
            </div>
        </body>
        </html>
        """

        send_email(article_version_author['email'], "Your Article Version Has Been Deleted!", body_article_version_author)

        if article_version_author['email'] != article_author['email']:
            send_email(article_author['email'], "A Version of Your Article Has Been Deleted!", body_article_author)

    async def restore_article_version_v3(
        self,
        article_id: StrictStr,
        version_id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
    ) -> None:

        article = await mongodb["article"].find_one({"_id": ObjectId(article_id)},
                                                    {"versions._id": 1, "versions.modification_date": 1, "wiki_id": 1})

        wiki_author = await get_wiki_author(str(article["wiki_id"]))

        if not admin and user_id != wiki_author["id"] and user_id != str(article["author"]["_id"]):
            raise Exception("User can't restore this article version")

        """Restore an older ArticleVersion of an Article."""
        user = await get_user(user_id)
        restored_version = await mongodb["article_version"].find_one({"_id": ObjectId(version_id)})
        article_author = await get_user(article["author"]["_id"])

        body_restore_article_version = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 0;">
            <div style="background-color: #ffc107; color: white; padding: 20px; text-align: center;">
            <h1 style="margin: 0;">Your Article Has Been Restored!</h1>
            <p style="margin: 10px 0;">The user with email <strong>{user['email']}</strong> has restored an older version of your article.</p>
            </div>
            
            <div style="padding: 20px; background-color: #ffffff;">
            <h2 style="color: #ffc107;">Restoration Details</h2>
            <p><strong>Restored Article Version:</strong> <em>{restored_version["title"]}</em></p>
            <p><strong>Restored Article Version Author:</strong> <em>{restored_version['author']['name']}</em></p>
            <p>Please review the restored content to ensure it meets your expectations.</p>
            </div>
        </body>
        </html>
        """


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

        for id_version in version_ids_to_delete:
            await _delete_article_translation(id_version)
        
        send_email(article_author['email'], "Your Article Has Been Restored!", body_restore_article_version)

        return None