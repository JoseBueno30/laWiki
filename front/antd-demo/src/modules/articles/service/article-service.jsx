import APIGateway from "../../../interceptor/interceptor"

const ArticleService = () =>{
    const getArticleVersionByName = async (wiki_id, name, lan) =>{
        try{
            const params = new URLSearchParams({wiki: wiki_id, lan: lan})
            const url = `v1/articles/versions/by-name/${name}?${params.toString()}`

            const response = await APIGateway.get(url)
            return response
        }catch(error){
            console.error("ArticleService.getArticleVersionByName: ", error)
            return Promise.reject(error)
        }
    }

    const getArticleVersionsByArticleID = async (article_id) =>{
        try{
            const url = `v1/articles/${article_id}/versions`
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
            const url = `v1/articles/versions/${articleVersionId}?${params.toString()}`

            const response = await APIGateway.get(url)
            return response
        }catch(error){
            console.error("ArticleService.getArticleVersionByID:", error)
            return Promise.reject(error)
        }
    }

    const restoreArticleVersion = async (articleId, versionId) =>{
        try{
            const url = `v1/articles/${articleId}/versions/${versionId}`

            const response = await APIGateway.put(url)
            return response
        }catch(error){
            console.error("ArticleService.getArticleVersionByID:", error)
            return Promise.reject(error)
        }
    }

    return {
        getArticleVersionByName,
        getArticleVersionsByArticleID,
        getArticleVersionByID,
        restoreArticleVersion
    }
}

export default ArticleService