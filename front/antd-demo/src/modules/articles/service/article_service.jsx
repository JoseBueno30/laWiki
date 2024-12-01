import axios from "axios";


const APIGateway = axios.create({
    baseURL: "http://localhost:3000",
    timeout: 5000,
    headers: {
        "Content-Type": "application/json",
    },
});

APIGateway.interceptors.response.use(
    (response) => {
        return response.data;
    },
    (error) => {
        console.error("Error:", error);
        if (error.response) {
            return Promise.reject(error.response.data);
        } else if (error.request) {
            return Promise.reject({
                message: "Error with no response",
            });
        } else {
            return Promise.reject({ message: error.message });
        }
    }
);

const searchArticlesWithParams = async (queryParams) => {
    try {
        return await APIGateway.get("http://localhost:3000/v1/articles", {
            params: queryParams,
        });
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};

const searchArticlesWithPaginationURL = async (paginationURL) => {
    try {
        return await APIGateway.get("http://localhost:3000/v1" + paginationURL);
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
  };
  
export {searchArticlesWithParams, searchArticlesWithPaginationURL};