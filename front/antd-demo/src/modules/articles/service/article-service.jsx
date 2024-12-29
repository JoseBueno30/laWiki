import APIGateway from "../../../interceptor/interceptor"

const ArticleService = () =>{

    function serializeParams(params) {
        return Object.entries(params)
          .map(([key, value]) => 
            Array.isArray(value) 
              ? value.map(val => `${key}=${encodeURIComponent(val)}`).join('&') 
              : `${key}=${encodeURIComponent(value)}`
          )
          .join('&');
      }

    const getArticleVersionByName = async (wiki_id, name, lan) =>{
        try{
            const params = new URLSearchParams({wiki: wiki_id})
            if (lan) params.append("lan", lan)
            
            const url = `/articles/versions/by-name/${name}?${params.toString()}`

            const response = await APIGateway.get(url)
            return response
        }catch(error){
            console.error("ArticleService.getArticleVersionByName: ", error)
            return Promise.reject(error)
        }
    }

    const getArticleVersionsByArticleID = async (article_id, order) =>{
        try{
            const params = new URLSearchParams({
                order: order
            })
            const url = `/articles/${article_id}/versions?${params.toString()}`
            const response = await APIGateway.get(url)
            return response
        }catch(error){
            console.error("ArticleService.getArticleVersionsByArticleID: ", error)
            return Promise.reject(error)
        }
    }

    const getArticleVersionByID = async (articleVersionId, lan) =>{
        try{
            const params = new URLSearchParams({lan: lan})
            const url = `/articles/versions/${articleVersionId}?${params.toString()}`

            const response = await APIGateway.get(url)
            return response
        }catch(error){
            console.error("ArticleService.getArticleVersionByID:", error)
            return Promise.reject(error)
        }
    }

    const restoreArticleVersion = async (articleId, versionId) =>{
        try{
            const url = `/articles/${articleId}/versions/${versionId}`

            const response = await APIGateway.put(url)
            return response
        }catch(error){
            console.error("ArticleService.getArticleVersionByID:", error)
            return Promise.reject(error)
        }
    }

    const getArticleById = async (articleId) =>{
        try{
            const url = `/articles/${articleId}`
            const response = await APIGateway.get(url)
            return response
        }catch(error){
            console.error("ArticleService.getArticleByID:", error)
            return Promise.reject(error)
        }
    }

    const uploadImage = async(file) =>{
        try {
            const formData = new FormData();
            formData.append('file', file);
    
            const response = await APIGateway.post("/upload-image", formData, {
                headers: {
                  'Content-Type': 'multipart/form-data',
                },
            });
    
            return response.url
        } catch (error) {
            return Promise.reject(error)
        }
    }
    
    const searchArticlesWithParams = async (queryParams) => {
        try {
            return await APIGateway.get(`/articles?${serializeParams(queryParams)}`);
        } catch (error) {
            return Promise.reject(error)
        }
    };
    
    const searchArticlesByAuthor = async (author_id,queryParams) => {
        try {
            return await APIGateway.get(`/articles/author/${author_id}`, {
                params: queryParams,
            });
        } catch (error) {
            return Promise.reject(error)
        }
    };
    
    const searchArticlesWithPaginationURL = async (paginationURL) => {
        try {
            return await APIGateway.get(paginationURL);
        } catch (error) {
            return Promise.reject(error)
        }
      };
    
    const getWikiTags = async(wikiId) =>{
        try {
    
            var response = await APIGateway.get("/tags/wikis/" + wikiId);
    
            var tagList = response.articles; //Misspelling of the API, it is a list of tags
    
            while (response.next != null){
                response = await APIGateway.get(response.next);
                tagList = [...tagList, ...response.articles];
            }
    
            tagList = tagList.map(tag => ({
                id: tag.id,
                tag: tag.translations
              }));
    
            return tagList;
        } catch (error) {
            return Promise.reject(error)
        }
    }
    
    const createArticleVersion = async(articleId, newArticleVersion) =>{
        try {
    
            return await APIGateway.post("/articles/" + articleId + "/versions", newArticleVersion);
    
        } catch (error) {
            return Promise.reject(error)
        }
    }
    
    const createArticle = async(newArticle) =>{
        try {
    
            return await APIGateway.post("/articles", newArticle);
    
        } catch (error) {
            return Promise.reject(error)
        }
    }
    
    const getArticleWikiTextBody = async(articleId, lan) =>{
        try {
            const params = {
                parsed: false,
                lan: lan
            }
    
            return await APIGateway.get("/articles/versions/"+ articleId + "/body", {params:params});
    
        } catch (error) {
            return Promise.reject(error)
        }
    }

    const deleteArticleByID = async(articleId) =>{
        try {
            return await APIGateway.delete("/articles/"+ articleId);
        } catch (error) {
            return Promise.reject(error)
        }
    }

    return {
        getArticleVersionByName,
        getArticleVersionsByArticleID,
        getArticleVersionByID,
        restoreArticleVersion,
        getArticleById,
        searchArticlesWithParams,
        searchArticlesByAuthor,
        searchArticlesWithPaginationURL, 
        uploadImage, 
        getWikiTags, 
        createArticleVersion, 
        createArticle, 
        getArticleWikiTextBody,
        deleteArticleByID
    }
}

export default ArticleService