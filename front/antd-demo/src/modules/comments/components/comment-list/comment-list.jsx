
import React, { useEffect, useState } from 'react';
import './comment-list.css';
import { CommentOutlined, SortAscendingOutlined, ControlOutlined} from '@ant-design/icons';
import { Flex, Space, Typography, Radio, DatePicker, Button} from 'antd';
import CommentInput from '../comment-input/comment-input';
import Comment from '../comment/comment';
import { Pagination } from 'antd';


const {Text, _ } = Typography
const {RangePicker} = DatePicker

// const user = {
//   name: "Adriduty",
//   image: "https://i1.sndcdn.com/artworks-ynfN32NPS8zDyraR-PHw2zQ-t500x500.jpg",
//   id: "1"
// }

const options = [
  { label: 'recent', value: 'recent' },
  { label: 'oldest', value: 'oldest' }
];

const CommentList = ({commentsObject, user, fetchFunc}) => {
  // console.log("COMMENT LIST", comments)

  const [commentList, setCommentList] = useState(commentsObject.comments)
  const [paginationIndex, setPaginationIndex] = useState(1)

  useEffect(() =>{
    setCommentList(commentsObject.comments)
  },[commentsObject])

  const range = (start, end) => Array.from({ length: end - start + 1 }, (_, i) => start + i);

  const handlePaginationChange = (page, PageSize) =>{
    fetchFunc(page-1, null)
  }

  return (
    
    <Flex className='comment-list'>
      <Space direction='vertical' style={{width: "100%"}}>
        <Space className='comment-list-title comment-list-son'>
          <CommentOutlined className='icon'></CommentOutlined>
          <Text strong>Comments ({commentList.length})</Text>
        </Space>

        <CommentInput user={user}></CommentInput>

        <div className='comment-list-options'>
          <Space className='comment-list-title comment-list-son'>
            <SortAscendingOutlined style={{fontSize: "25px"}}/>
            <Text strong>Order</Text>
      
            <Radio.Group block size='small' options={options} defaultValue="recent" optionType='button'/>
          </Space>
          <Space className='filter-group'>
              <ControlOutlined className='icon comment-list-son'/>
              <Text className='comment-list-son' strong>Filter</Text>
              <Text className='comment-list-son'>Date Range</Text>
              <RangePicker  allowEmpty={[true, true]}/>
          </Space>
        </div>
        {
          commentList.map((element, index) => (
            <Comment key={index} comment={element}></Comment>
          ))
        }
        {console.log(commentsObject)}
        <Flex align='center' justify='center' gap={3}>
          {console.log("LIMITE", (commentsObject.total / commentsObject.limit) + 1)}
          <Pagination size='small' gap={3} pageSize={3} defaultCurrent={1} total={6} onChange={handlePaginationChange} />
        </Flex>
      </Space>
      
    </Flex>
  );
};

export default CommentList;
