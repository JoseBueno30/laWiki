
import React from 'react';
import './comment-list.css';
import { CommentOutlined, SortAscendingOutlined, ControlOutlined} from '@ant-design/icons';
import { Flex, Space, Typography, Radio, DatePicker} from 'antd';
import CommentInput from '../comment-input/comment-input';
import Comment from '../comment/comment';

const {Text, _ } = Typography
const {RangePicker} = DatePicker

const user = {
  name: "Adriduty",
  image: "https://i1.sndcdn.com/artworks-ynfN32NPS8zDyraR-PHw2zQ-t500x500.jpg",
  id: "1"
}

const options = [
  { label: 'recent', value: 'recent' },
  { label: 'oldest', value: 'oldest' }
];

const CommentList = ({commentList = [   ]}) => {
  console.log(commentList)
  return (
    
    <Flex  style={{padding: "20px", width: "80%"}}>
      <Space direction='vertical' style={{width: "100%"}}>
        <Space className='comment-list-title'>
          <CommentOutlined className='icon'></CommentOutlined>
          <Text strong>Comments (3)</Text>
        </Space>

        <CommentInput user={user}></CommentInput>

        <div className='comment-list-options'>
          <Space className='comment-list-title'>
            <SortAscendingOutlined style={{fontSize: "25px"}}/>
            <Text strong>Order</Text>
      
            <Radio.Group block size='small' options={options} defaultValue="recent" optionType='button'/>
          </Space>
          <Space className='filter-group'>
              <ControlOutlined className='icon'/>
              <Text strong style={{paddingRight: "1.5rem"}}>Filter</Text>
              <Text>Date Range</Text>
              <RangePicker/>
          </Space>
        </div>
        {
          commentList.map((element, index) => (
            <Comment key={index} comment={element}></Comment>
          ))
        }

      </Space>
      
    </Flex>
  );
};

export default CommentList;
