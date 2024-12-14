import { Avatar, Image } from "antd";
import "./UserTop.css";

const UserTop = ({user_picture="", user_name=""}) => {
    const picture = <Image
    className="userAvatar"
    src={user_picture} 
    alt={`Profile picture for ${user_name}`}
    />;
    
    const title = <figcaption className="userName">{user_name}</figcaption>
    return(
    <figure className="userFigure">
        {picture}
        {title}
    </figure>);
}
export default UserTop;