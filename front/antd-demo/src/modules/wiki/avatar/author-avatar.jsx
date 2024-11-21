import { Avatar, Flex, Typography } from 'antd';
import Title from 'antd/es/typography/Title';

const { Text } = Typography;

const AuthorAvatar = ({ image, username, role }) => {
  return (
    <Flex gap='small' align='center'>
      <Avatar
        src={image} // Ajusta el tamaño del avatar
        size={64}
        alt={`${username}'s avatar`}
      />
      <Flex vertical>
        <Text style={{fontSize: '20px', fontWeight: 'bold'}}>{username}</Text>
        <Text >{role}</Text>
      </Flex>
    </Flex>
  );
};


export default AuthorAvatar;