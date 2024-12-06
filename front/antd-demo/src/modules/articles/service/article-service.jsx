import APIGateway from "../../../interceptor/interceptor"

const ArticleService = () =>{
    const getArticleVersionByName = async (wiki_id, name, lan) =>{
        try{
            const params = new URLSearchParams({wiki: wiki_id})
            if (lan) params.append("lan", lan)
            
            const url = `v1/articles/versions/by-name/${name}?${params.toString()}`

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
            const url = `v1/articles/${article_id}/versions?${params.toString()}`
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

    const getArticleById = async (articleId) =>{
        try{
            const url = `v1/articles/${articleId}`
            const response = await APIGateway.get(url)
            return response
        }catch(error){
            console.error("ArticleService.getArticleByID:", error)
            return Promise.reject(error)
        }
    }

    return {
        getArticleVersionByName,
        getArticleVersionsByArticleID,
        getArticleVersionByID,
        restoreArticleVersion,
        getArticleById
    }
}

export default ArticleService