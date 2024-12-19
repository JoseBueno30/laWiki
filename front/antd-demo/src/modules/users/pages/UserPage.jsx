import UserTop from "../components/UserTop/UserTop";
import UserContent from "../components/UserContent/UserContent";

const UserPage = () => {
    let userName = "DefaultAuthor";
    let userId = "672901e41a1c2dc79c930dee";

    return(<div>
        <UserTop user_picture="https://picsum.photos/500" user_name={userName} />
        <UserContent author_name={userName} author_id={userId}/>
    </div>);
}
export default UserPage;