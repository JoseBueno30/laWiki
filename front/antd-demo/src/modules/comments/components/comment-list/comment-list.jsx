
import React, { useEffect, useState } from 'react';
import './comment-list.css';
import { CommentOutlined, SortAscendingOutlined, ControlOutlined, SearchOutlined} from '@ant-design/icons';
import { Flex, Space, Typography, Radio, DatePicker, Button} from 'antd';
import CommentInput from '../comment-input/comment-input';
import Comment from '../comment/comment';
import { Pagination } from 'antd';
import { useTranslation } from 'react-i18next';

const dateFormat = "YYYY/MM/DD";

const {Text, _ } = Typography
const {RangePicker} = DatePicker

// const user = {
//   name: "Adriduty",
//   image: "https://i1.sndcdn.com/artworks-ynfN32NPS8zDyraR-PHw2zQ-t500x500.jpg",
//   id: "1"
// }

const CommentList = ({commentsObject, user, fetchFunc}) => {
  // console.log("COMMENT LIST", comments)
  const {t} = useTranslation()

  const [commentList, setCommentList] = useState(commentsObject.comments)
  const [currentPage, setCurrentPage] = useState(1);
  const [order, setOrder] = useState('recent')
  const [dateRange, setDateRange] = useState(null)

  const options = [
    { label: t('common.order-recent'), value: 'recent' },
    { label: t('common.order-oldest'), value: 'oldest' }
  ];

  useEffect(() =>{
    setCommentList(commentsObject.comments)
  },[commentsObject])

  const handlePaginationChange = (page, _) =>{
    setCurrentPage(page)
    fetchFunc((page-1) * commentsObject.limit, order, dateRange)
  }

  const handleOrderChange = (e) =>{
    setCurrentPage(1)
    setOrder(e.target.value)
    fetchFunc(0, e.target.value, dateRange)
  }

  const generateDateRange = (startDate, endDate) =>
    startDate && endDate
      ? `${startDate}-${endDate}`
      : startDate
      ? `${startDate}`
      : endDate
      ? `${endDate}`
      : null;

  const handleDateRangeChange = (_, time) =>{
    const range = generateDateRange(time[0], time[1])
    setDateRange(range)
    fetchFunc(0, order, range)
  }

  return (
    
    <Flex className='comment-list'>
      <Space direction='vertical' style={{width: "100%"}}>
        <Space className='comment-list-title comment-list-son'>
          <CommentOutlined className='icon'></CommentOutlined>
          <Text strong>{t('article.comments-header', {count: commentList.length})}</Text>
        </Space>

        <CommentInput user={user}></CommentInput>

        <div className='comment-list-options'>
          <Space className='comment-list-title comment-list-son'>
            <SortAscendingOutlined style={{fontSize: "25px"}}/>
            <Text strong>{t('common.order-header')}</Text>
      
            <Radio.Group onChange={handleOrderChange} block size='small' options={options} defaultValue="recent" optionType='button'/>
          </Space>
          <Space className='filter-group'>
              <ControlOutlined className='icon comment-list-son'/>
              <Text className='comment-list-son' strong>{t('common.filter-header')}</Text>
              <Text className='comment-list-son'>{t('common.daterange-header')}</Text>
              <Space.Compact>
                <RangePicker format={dateFormat} allowEmpty={[true, true]} onChange={handleDateRangeChange}/>
                {/* <Button icon={<SearchOutlined/>}></Button> */}
              </Space.Compact>
              
          </Space>
        </div>
        {
          commentList.map((element, index) => (
            <Comment key={index} comment={element}></Comment>
          ))
        }
        <Flex align='center' justify='center' gap={3}>
          {commentsObject.comments.length > 0 ? 
            <Pagination size='small' gap={3} pageSize={3} defaultCurrent={currentPage} current={currentPage} total={commentsObject.total} onChange={handlePaginationChange}/> 
            : ""
          }
        </Flex>
      </Space>
      
    </Flex>
  );
};

export default CommentList;
