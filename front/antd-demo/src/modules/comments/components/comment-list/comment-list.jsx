
import React from 'react';
import './comment-list.css';
import { CommentOutlined, SortAscendingOutlined, ControlOutlined} from '@ant-design/icons';
import { Flex, Space, Typography, Radio, DatePicker} from 'antd';
import CommentInput from '../comment-input/comment-input';
import Comment from '../comment/comment';

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

const CommentList = ({commentList, user}) => {
  console.log("COMMENT LIST", commentList)
  return (
    
    <Flex className='comment-list'>
      <Space direction='vertical' style={{width: "100%"}}>
        <Space className='comment-list-title comment-list-son'>
          <CommentOutlined className='icon'></CommentOutlined>
          <Text strong>Comments (3)</Text>
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

      </Space>
      
    </Flex>
  );
};

export default CommentList;
