import axios from "axios";
import APIGateway from "../../../interceptor/interceptor";


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