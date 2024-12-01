
import React from 'react';
import './wiki-sidebar.css';
import Sider from 'antd/es/layout/Sider';
import { Flex, Rate, Grid } from 'antd';
import RoleAvatar from '../avatar/role-avatar';
const { useBreakpoint } = Grid;


const WikiSidebar = (example) => {

  const screens = useBreakpoint();

  return (
    <Sider className='wiki-sidebar'>
        <Flex align='center' vertical>
          <img src={example.image}></img>
          <div className='rating-container'>
            <b>{example.rating}</b>
            <Rate style={{ marginLeft: 10 }} disabled allowHalf value={example.rating} />
          </div>
          <h2>{example.title}</h2>
          <span className='wiki-description'>{example.description}</span>
          <div className='user-container'>
            <RoleAvatar image={example.author.avatar} username={example.author.name} role='Author'/>
          </div>
        </Flex>
      </Sider>
  );
};

export default WikiSidebar;
