
import React from 'react';
import './comment-input.css';
import '../comment/comment.css'
import { Avatar, Flex, Input, Space, Typography, Button } from 'antd';
const { Text, Paragraph } = Typography;
const {TextArea} = Input

const CommentInput = ({user}) => {
  return (
    <Flex className='comment-input comment-list-son'>
      <Avatar className='comment-avatar' src={user.image} alt={user.name} />
      <div style={{width: "100%"}}>
        <Space style={{width: "100%"}} direction="vertical">
          <TextArea showCount maxLength={200} size='large' autoSize = {{minRows: 3}}/>
          <Button type='primary'>Subir</Button>
        </Space>
      </div>
    </Flex>
  );
};

export default CommentInput;
