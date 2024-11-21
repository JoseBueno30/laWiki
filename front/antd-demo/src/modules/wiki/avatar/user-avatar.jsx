import { Avatar, Flex, Typography } from 'antd';

const { Text } = Typography;

const UserAvatar = ({ image, username }) => {
  return (
    <Flex gap='small' align='center'>
      <Avatar
        src={image} // Ajusta el tamaño del avatar
        alt={`${username}'s avatar`}
      />
      <Text >{username}</Text>
    </Flex>
  );
};


export default UserAvatar;
