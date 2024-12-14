import { useEffect, useState } from "react";
import UserTop from "../components/UserTop/UserTop";
import UserContent from "../components/UserContent/UserContent";
import WikiService from "../../wiki/service/wiki-service";
import ArticleService from "../../articles/service/article-service";

const { searchWikisWithParams } = WikiService();
const { searchArticlesWithParams } = ArticleService();//Tengo que cambiar el método este requiere wiki

const UserPage = () => {
    let userName = "DefaultAuthor";
    const [articles,setArticles] = useState([])
    const [wikis,setWikis] = useState([])

    const getParams = () => {
        return { "author_name" : userName }
    }
    useEffect(() => {
        const params = getParams();
        searchWikisWithParams(params).then((response) => {
            setWikis(response.wikis);
        });
        searchArticlesWithParams(params).then((response) => {
            setArticles(response.articles);
        });
    },[])
    return(<div>
        <UserTop user_picture="https://picsum.photos/500" user_name={userName} />
        <UserContent articles={articles} wikis={wikis}/>
    </div>);
}
export default UserPage;