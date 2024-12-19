import UserTop from "../components/UserTop/UserTop";
import UserContent from "../components/UserContent/UserContent";

const UserPage = () => {
    let userName = "DefaultAuthor";

    return(<div>
        <UserTop user_picture="https://picsum.photos/500" user_name={userName} />
        <UserContent author_name={userName}/>
    </div>);
}
export default UserPage;