import axios from "axios";
import APIGateway from "../../../interceptor/interceptor";

const uploadImage = async(file) =>{
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await APIGateway.post("http://localhost:3000/v1/upload-image", formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
        });

        return response.url
    } catch (error) {
        throw new Error('Error uploading file: ' + error.message);
    }
}
    

const searchArticlesWithParams = async (queryParams) => {
    try {
        return await APIGateway.get("http://localhost:3000/v1/articles", {
            params: queryParams,
        });
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};

const searchArticlesWithPaginationURL = async (paginationURL) => {
    try {
        return await APIGateway.get("http://localhost:3000/v1" + paginationURL);
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
  };

const getWikiTags = async(wikiId) =>{
    try {

        var response = await APIGateway.get("http://localhost:3000/v1/tags/wikis/" + wikiId);

        var tagList = response.articles; //Misspelling of the API, it is a list of tags

        while (response.next != null){
            response = await APIGateway.get("http://localhost:3000/v1" + response.next);
            tagList = [...tagList, ...response.articles];
        }

        tagList = tagList.map(tag => ({
            id: tag.id,
            tag: tag.translations
          }));

        return tagList;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

const createArticleVersion = async(articleId, newArticleVersion) =>{
    try {

        return await APIGateway.post("http://localhost:3000/v1/articles/" + articleId + "/versions", newArticleVersion);

    } catch (error) {
        throw new Error('Error creating ArticleVersion: ' + error.message);
    }
}

const createArticle = async(newArticle) =>{
    try {

        return await APIGateway.post("http://localhost:3000/v1/articles", newArticle);

    } catch (error) {
        throw new Error('Error creating Article: ' + error.message);
    }
}

const getArticleWikiTextBody = async(articleId, lan) =>{
    try {
        const params = {
            parsed: false,
            lan: lan
        }

        return await APIGateway.get("http://localhost:3000/v1/articles/versions/"+ articleId + "/body", {params:params});

    } catch (error) {
        throw new Error('Error: ' + error.message);
    }
}
  
export {searchArticlesWithParams, searchArticlesWithPaginationURL, uploadImage, getWikiTags, createArticleVersion, createArticle, getArticleWikiTextBody};