import { UserOutlined } from '@ant-design/icons';
import { Avatar, Flex, Typography } from 'antd';
import { useNavigate } from 'react-router-dom';

const { Text } = Typography;

const RoleAvatar = ({ id, image, username, role }) => {
  const navigate = useNavigate();

  const goToUser = () => {
    navigate(`/users/${id}`);
  };
  return (
    <Flex gap='small' align='center'>
      <Avatar
        icon = {image ? null : <UserOutlined/>}
        src={image}
        size={64}
        alt={`${username ? username : "Username"}'s avatar`}
        className='role-avatar'
        style={{cursor: 'pointer'}}
        onClick={goToUser}
      />
      <Flex vertical>
        <Text onClick={goToUser} style={{fontSize: '20px', fontWeight: 'bold',cursor: 'pointer'}}>{username ? username : "Username"}</Text>
        <Text >{role ? role : "User Role"}</Text>
      </Flex>
    </Flex>
  );
};


export default RoleAvatar;