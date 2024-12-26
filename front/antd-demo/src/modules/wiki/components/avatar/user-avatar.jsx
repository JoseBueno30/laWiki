import { Avatar, Flex, Typography } from "antd";
import { UserOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

const { Text } = Typography;

const UserAvatar = ({ id, image, username, justify }) => {
  const navigate = useNavigate();

  const goToUser = (e) => {
    e.stopPropagation();
    navigate(`/users/${id}`);
  };

  return (
    <Flex gap="small" align="center" justify={justify}>
        <Avatar
          icon={image ? null : <UserOutlined />} // Si no hay imagen, muestra el icono de usuario
          src={image} // Ajusta el tamaño del avatar
          alt={`${username ? username : "Username"}'s avatar`}
          onClick={() => goToUser()}
        />
      <Text onClick={goToUser}>{username ? username : "Username"}</Text>
    </Flex>
  );
};

export default UserAvatar;
