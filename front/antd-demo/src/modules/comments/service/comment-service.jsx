import APIGateway from "../../../interceptor/interceptor"

const CommentService = () =>{
    const getArticleComments = async (articleId, offset, limit, order, creationDate) =>{
        try{
            const params = new URLSearchParams({
                order: order,
                limit: limit,
                offset: offset
            })
            if (creationDate != null){
                params.append("creation_date", creationDate)
            }

            const url = `/comments/articles/${articleId}?${params.toString()}`
            
            const response = await APIGateway.get(url);
            return response
        }catch(error){
            console.error("CommentService.getArticleComments:", error)
            return Promise.reject(error)
        }
    }

    const postComment = async (articleId, userId, body) => {
        try{
            const params = {
                author_id: userId,
                body: body
            }
    
            const url = `/comments/articles/${articleId}`
    
            const response = await APIGateway.post(url, params)
            return response
        }catch(error){
            console.error("CommentService.PostComment:", error)
            return Promise.reject(error)
        }
    }

    const deleteComment = async (commentId) =>{
        try{
            const url = `/comments/${commentId}`

            const response = await APIGateway.delete(url)
            return response
        }catch(error){
            console.error("CommentService.DeleteComment:", error)
            return Promise.reject(error)
        }
    }

    return {
        getArticleComments, postComment, deleteComment
    }
}

export default CommentService