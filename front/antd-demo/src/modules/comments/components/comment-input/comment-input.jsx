
import React, { useState } from 'react';
import './comment-input.css';
import '../comment/comment.css'
import { Avatar, Flex, Input, Space, Button } from 'antd';
import CommentService from '../../service/comment-service';
import { useTranslation } from 'react-i18next';

const {TextArea} = Input

const CommentInput = ({user, uploadFunc}) => {
  const { t } = useTranslation();
  const [text, setText] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const uploadComment = async () =>{
    setSubmitting(true)
    await uploadFunc(text)
    setSubmitting(false)
    setText('')
  }

  return (
    <Flex className='comment-input comment-list-son'>
      <Avatar className='comment-avatar' src={user.image} alt={user.name} />
      <div style={{width: "100%"}}>
        <Space style={{width: "100%"}} direction="vertical">
          <TextArea value={text} showCount maxLength={200} size='large' autoSize = {{minRows: 3}} onChange={(e) => {setText(e.target.value)}}/>
          <Button onClick={uploadComment} type='primary' loading={submitting ? true : false} iconPosition='end'>{t('article.post-comment-button')}</Button>
        </Space>
      </div>
    </Flex>
  );
};

export default CommentInput;
