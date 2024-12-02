import apiClient from "../../../interceptor/interceptor"

const CommentsService = () =>{
    const getArticleComments = async (articleId, offset, creationDate) =>{
        try{
            const params = new URLSearchParams({
                limit: 20,
                offset: offset
            })
            const url = `/v1/comments/articles/${articleId}?${params.toString()}`
            
            const response = await apiClient.get(url);
            return response
        }catch(error){
            console.error("CommentService.getArticleComments:", error)
            return Promise.reject(error)
        }
    }

    return {
        getArticleComments
    }
}

export default CommentsService