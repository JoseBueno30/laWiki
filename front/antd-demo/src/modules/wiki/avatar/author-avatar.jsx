import { UserOutlined } from '@ant-design/icons';
import { Avatar, Flex, Typography } from 'antd';

const { Text } = Typography;

const AuthorAvatar = ({ image, username, role }) => {
  return (
    <Flex gap='small' align='center'>
      <Avatar
        icon = {image ? null : <UserOutlined/>}
        src={image}
        size={64}
        alt={`${username ? username : "Username"}'s avatar`}
      />
      <Flex vertical>
        <Text style={{fontSize: '20px', fontWeight: 'bold'}}>{username ? username : "Username"}</Text>
        <Text >{role ? role : "User Role"}</Text>
      </Flex>
    </Flex>
  );
};


export default AuthorAvatar;