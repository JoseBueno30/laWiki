
import React from 'react';
import './wiki-sidebar.css';
import Sider from 'antd/es/layout/Sider';
import { Flex, Rate, Grid } from 'antd';
import RoleAvatar from '../avatar/role-avatar';
const { useBreakpoint } = Grid;


const WikiSidebar = (wiki) => {
  wiki = wiki.wiki;

  return (
    <Sider className='wiki-sidebar'>
        <Flex align='center' vertical>
          <img src={wiki.image}></img>
          <div className='rating-container'>
            <b>{wiki.rating}</b>
            <Rate style={{ marginLeft: 10 }} disabled allowHalf value={wiki.rating} />
          </div>
          <h2>{wiki.title}</h2>
          <span className='wiki-description'>{wiki.description}</span>
          <div className='user-container'>
            <RoleAvatar image={wiki.author.image} username={wiki.author.name} role='Author'/>
          </div>
        </Flex>
      </Sider>
  );
};

export default WikiSidebar;
