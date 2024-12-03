import axios from "axios";
import APIGateway from "../../../interceptor/interceptor";

const uploadImage = async(file) =>{
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await APIGateway.post("http://localhost:3000/v1/upload-image", formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
        });

        return response.data.url
    } catch (error) {
        throw new Error('Error uploading file: ' + error.message);
    }
}
    

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
  
export {searchArticlesWithParams, searchArticlesWithPaginationURL, uploadImage};