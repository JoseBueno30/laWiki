import { Avatar, Flex, Typography } from "antd";
import { UserOutlined } from "@ant-design/icons";

const { Text } = Typography;

const UserAvatar = ({ image, username }) => {
  return (
    <Flex gap="small" align="center">
      <Avatar
        icon = {image ? null : <UserOutlined />} // Si no hay imagen, muestra el icono de usuario
        src={image} // Ajusta el tamaño del avatar
        alt={`${username ? username : "Username"}'s avatar`}
      />
      <Text>{username ? username : "Username"}</Text>
    </Flex>
  );
};

export default UserAvatar;
