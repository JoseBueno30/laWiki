
import React from 'react';
import './comment.css';
import {Avatar, Button, Flex, Space, Typography} from 'antd';
import { DeleteOutlined } from '@ant-design/icons';

const { Text, Paragraph } = Typography;

const Comment = ({comment, user, deleteFunc}) => {

  const deleteComment = () =>{
    deleteFunc(comment.id)
  }

  return (
    <Flex className='comment-list-son'>
      <Flex>
        <Avatar className='comment-avatar' src={comment.author.image} alt={comment.author.name} />
      </Flex>
      <Flex className='comment-container' align='center' justify='space-between'>
        <div>
          <Space direction="vertical">
            <Space>
              <Text strong>{comment.author.name}</Text>
              <Text type="secondary">{comment.creation_date}</Text>
            </Space>
            <Paragraph ellipsis={{rows: 5}}
              style={{ whiteSpace: 'normal', wordWrap: 'break-word', overflowWrap: 'break-word' }}
              >
                {comment.body}
              </Paragraph>
          </Space>
        </div>

        {user && user.id == comment.author.id ? 
          <Button onClick={deleteComment} className='delete-comment-button' danger icon={<DeleteOutlined/>}></Button>
          :
          ""
        }
        
      </Flex>
    </Flex>
  );
};

export default Comment;
