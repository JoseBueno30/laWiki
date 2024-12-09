
import React from 'react';
import './comment.css';
import {Avatar, Flex, Space, Typography} from 'antd';

const { Text, Paragraph } = Typography;

const Comment = ({comment}) => {
  return (
    <Flex className='comment-list-son'>
      <Flex>
        <Avatar className='comment-avatar' src={comment.author.image} alt={comment.author.name} />
      </Flex>
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
    </Flex>
  );
};

export default Comment;
