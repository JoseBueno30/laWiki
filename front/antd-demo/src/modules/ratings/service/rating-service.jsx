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
    
    return{
        getArticleRatings
    }
}

export default RatingService