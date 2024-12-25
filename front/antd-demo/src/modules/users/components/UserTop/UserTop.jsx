import { Avatar, Image, Rate } from "antd";
import "./UserTop.css";

const UserTop = ({user_picture="", user_name="", user_rating=0}) => {
    const picture = <Image
    className="userAvatar"
    src={user_picture} 
    alt={`Profile picture for ${user_name}`}
    />;
    
    const rating = <Rate disabled allowHalf value={user_rating} />;
    console.log(user_rating);

    const title = <figcaption spellCheck={false} className="userName">{user_name}</figcaption>

    return(
    <figure className="userFigure">
        {picture}
        {title}
        {rating}
    </figure>);
}
export default UserTop;