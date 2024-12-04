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

        return response.data.url
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

        var tagList = response.data.articles; //Misspelling of the API, it is a list of tags

        while (response.data.next != null){
            response = await APIGateway.get("http://localhost:3000/v1" + response.data.next);
            tagList = [...tagList, ...response.data.articles];
        }

        return tagList;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

const createArticleVersion = async(articleId, newArticle) =>{
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await APIGateway.post("http://localhost:3000/v1/articles/" + articleId + "/versions", newArticle);

        return response.data.url
    } catch (error) {
        throw new Error('Error creating ArticleVersion: ' + error.message);
    }
}
  
export {searchArticlesWithParams, searchArticlesWithPaginationURL, uploadImage, getWikiTags, createArticleVersion};