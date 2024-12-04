
import React, { useState } from 'react';
import './comment-input.css';
import '../comment/comment.css'
import { Avatar, Flex, Input, Space, Button } from 'antd';
import CommentService from '../../service/comment-service';

const {TextArea} = Input

const CommentInput = ({user, uploadFunc}) => {

  const [text, setText] = useState('')

  const uploadComment = async () =>{
    await uploadFunc(text)
    setText('')
  }

  return (
    <Flex className='comment-input comment-list-son'>
      <Avatar className='comment-avatar' src={user.image} alt={user.name} />
      <div style={{width: "100%"}}>
        <Space style={{width: "100%"}} direction="vertical">
          <TextArea value={text} showCount maxLength={200} size='large' autoSize = {{minRows: 3}} onChange={(e) => {setText(e.target.value)}}/>
          <Button onClick={uploadComment} type='primary'>Subir</Button>
        </Space>
      </div>
    </Flex>
  );
};

export default CommentInput;
