import APIGateway from "../../../interceptor/interceptor"

const CommentService = () =>{
    const getArticleComments = async (articleId, offset, limit, order, creationDate) =>{
        try{
            const params = new URLSearchParams({
                order: order,
                limit: limit,
                offset: offset
            })
            const url = `/v1/comments/articles/${articleId}?${params.toString()}`
            
            const response = await APIGateway.get(url);
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

export default CommentService