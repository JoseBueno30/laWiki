import UserTop from "../components/UserTop/UserTop";
import UserContent from "../components/UserContent/UserContent";
import UserService from "../service/user-service";
import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
const { getUser } = UserService();

const UserPage = () => {
    let userId = "676698760a8531c3a4c20153"; //Se debe obtener de la sesión
    const { t } = useTranslation();
    const [userName, setUserName] = useState(t("common.loading-button"));
    const [userRating, setUserRating] = useState(0);
    const [userEmail, setUserEmail] = useState("");
    const [userImage, setUserImage] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getUser(userId).then((response) => {
            console.log(response);
            setUserName(response.username);
            setUserRating(response.rating);
            setUserEmail(response.email);
            setUserImage(response.image);
            setLoading(false);
        });
    }, []);


    return(<div className="userPage">
        <UserTop
        user_picture={userImage}
        user_name={userName}
        user_rating={userRating}/>
        {(loading) ? <></> : <UserContent author_name={userName} author_id={userId}/>}
    </div>);
}
export default UserPage;