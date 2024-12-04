import APIGateway from "../../../interceptor/interceptor"

const RatingService = () =>{

    const getArticleRatings = async (articleId) =>{
        try{

            const url = `/v1/ratings/articles/${articleId}/average`

            const response = await APIGateway.get(url)
            return response;
        }catch(error){
            console.error("RatingService.getArticleRatings:", error)
            return Promise.reject(error)
        }
    }

    const getUserRatingInArticle = async (userId, articleId) =>{
        try{
            const url = `/v1/ratings/articles/${articleId}/users/${userId}`

            const response = await APIGateway.get(url)
            return response
        }catch(error){
            console.log("RatingService.getUserRatingInArticle:", error)
            return null
        }
    }

    const updateArticleRating = async (articleId, authorId, value) =>{
        try{
            const params ={
                author_id: authorId,
                value: value
            };
            const url = `/v1/ratings/articles/${articleId}`

            const response = await APIGateway.put(url, params)
            return response
        }catch(error){
            console.error("RatingService.updateArticleRating:", error)
            return Promise.reject(error)
        }
    }

    const createArticleRating = async (articleId, authorId, value) =>{
        try{
            const params ={
                author_id: authorId,
                value: value
            };
            const url = `/v1/ratings/articles/${articleId}`

            const response = await APIGateway.post(url, params)
            return response
        }catch(error){
            console.error("RatingService.createArticleRating:", error)
            return Promise.reject(error)
        }
    }

    const deleteRating = async (ratingId) =>{
        try{
            const url = `/v1/ratings/${ratingId}`
        
            const response = await APIGateway.delete(url)
            return response
        }catch(error){
            console.error("RatingService.deleteRating:", error)
            return Promise.reject(error)
        }
    }
    
    return{
        getArticleRatings, getUserRatingInArticle, updateArticleRating, createArticleRating, deleteRating
    }
}

export default RatingService