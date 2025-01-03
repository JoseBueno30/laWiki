import UserTop from "../components/UserTop/UserTop";
import UserContent from "../components/UserContent/UserContent";
import UserService from "../service/user-service";
import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Flex, Spin } from "antd";

const { getUser } = UserService();

const UserPage = () => {
    let userId = useParams().user_id;
    const { t } = useTranslation();
    const [userName, setUserName] = useState("");
    const [userRating, setUserRating] = useState(0);
    const [userEmail, setUserEmail] = useState("");
    const [userImage, setUserImage] = useState("");
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    const navigateToNotFound = () => {
        navigate("/user_not_found");
    }

    useEffect(() => {
        getUser(userId).then((response) => {
            if (response.status === 404) {
                navigateToNotFound();
            } else {
                console.log(response);
                setUserName(response.username);
                setUserRating(response.rating);
                setUserEmail(response.email);
                setUserImage(response.image);
                setLoading(false);
            }
        }).catch((error) => {
            console.error("UserPage.getUser:", error);
            navigateToNotFound();
        });
    }, []);


    return(
        <Flex className="userMain" vertical align="center">
        {loading ? (
          <Spin size="large" style={{ paddingTop: "40vh" }} />
        ) : (
          
            <div className="userPage" style={{ width: "90%"}}>
            <UserTop
            user_picture={userImage}
            user_name={userName}
            user_rating={userRating}/>
            {(loading) ? <></> : <UserContent author_name={userName} author_id={userId}/>}
            </div>
        )}
      </Flex>
    );
    
}
export default UserPage;