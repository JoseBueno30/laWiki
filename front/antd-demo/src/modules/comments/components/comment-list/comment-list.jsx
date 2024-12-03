
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
  { label: 'Recent', value: 'recent' },
  { label: 'Oldest', value: 'oldest' }
];

const CommentList = ({commentsObject, user, fetchFunc}) => {
  // console.log("COMMENT LIST", comments)

  const [commentList, setCommentList] = useState(commentsObject.comments)
  const [currentPage, setCurrentPage] = useState(1);
  const [order, setOrder] = useState('recent')
  const [dateRange, setDateRange] = useState(null)

  useEffect(() =>{
    setCommentList(commentsObject.comments)
  },[commentsObject])

  const handlePaginationChange = (page, PageSize) =>{
    setCurrentPage(page)
    fetchFunc((page-1) * commentsObject.limit, order, null)
  }

  const handleOrderChange = (e) =>{
    print(e.target.value)
    setOrder(e.target.value)
    fetchFunc(0, e.target.value, null)
  }

  const handleDateRangeChange = (e) =>{

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
      
            <Radio.Group onChange={handleOrderChange} block size='small' options={options} defaultValue="recent" optionType='button'/>
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
          {commentsObject.comments.length > 0 ? 
            <Pagination size='small' gap={3} pageSize={3} defaultCurrent={currentPage} total={commentsObject.total} onChange={handlePaginationChange}/> 
            : ""
          }
        </Flex>
      </Space>
      
    </Flex>
  );
};

export default CommentList;
