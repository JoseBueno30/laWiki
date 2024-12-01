import apiClient from "../../../interceptor/interceptor"

const ArticleService = () =>{
    const getArticleVersionByName = async (wiki_id, name, lan) =>{
        try{
            const params = new URLSearchParams({wiki: wiki_id, lan: lan})
            console.log("PARAMS:", params)
            console.log("NAME:", name)
            const url = `v1/articles/versions/by-name/${name}?${params.toString()}`
            console.log("URL",url)
            const response = await apiClient.get(url)
            return response
        }catch(error){
            console.error("ArticleService.getArticleVersionByName: ", error)
            return Promise.reject(error)
        }
    }

    return {
        getArticleVersionByName
    }
}

export default ArticleService