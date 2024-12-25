import APIGateway from "../../../interceptor/interceptor"

const UserService = () => {
    
    const getUser = async (user_id) => {
        try{

            const url = `/v2/users/${user_id}`

            const response = await APIGateway.get(url)
            return response;
        }catch(error){
            console.error("UserService.getUser:", error)
            return Promise.reject(error)
        }
    }

    return {
        getUser
    }
};
export default UserService;
