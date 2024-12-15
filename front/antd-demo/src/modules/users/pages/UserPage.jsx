import { useEffect, useState } from "react";
import UserTop from "../components/UserTop/UserTop";
import UserContent from "../components/UserContent/UserContent";
import WikiService from "../../wiki/service/wiki-service";

const { searchWikisWithParams } = WikiService();

const UserPage = () => {
    let userName = "DefaultAuthor";
    const [wikis,setWikis] = useState([]);

    const getParams = () => {
        return { "author_name" : userName }
    }

    useEffect(() => {
        const params = getParams();
        searchWikisWithParams(params).then((response) => {
            setWikis(response.wikis);
        });
    },[]);

    return(<div>
        <UserTop user_picture="https://picsum.photos/500" user_name={userName} />
        <UserContent author_name={userName} wikis={wikis}/>
    </div>);
}
export default UserPage;