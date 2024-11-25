
import React from 'react';
import './comment-input.css';
import '../comment/comment.css'
import { Avatar, Flex, Input, Space, Typography, Button } from 'antd';
const { Text, Paragraph } = Typography;
const {TextArea} = Input

const CommentInput = ({user}) => {
  return (
    <Flex>
      <Avatar className='comment-avatar' src={user.image} alt={user.name} />
      <div style={{width: "100%"}}>
        <Space style={{width: "100%", paddingRight: "100px"}} direction="vertical">
          <Space>
            <Text strong>{user.name}</Text>
          </Space>    
          <TextArea size='large' autoSize = {{minRows: 2, maxRows: 3}}/>
          <Button type='primary'>Subir</Button>
        </Space>
      </div>
    </Flex>
  );
};

export default CommentInput;
