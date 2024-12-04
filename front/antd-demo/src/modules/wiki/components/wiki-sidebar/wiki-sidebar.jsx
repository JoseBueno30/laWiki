
import React from 'react';
import './wiki-sidebar.css';
import Sider from 'antd/es/layout/Sider';
import { Flex, Rate, Button, Image } from 'antd';
import RoleAvatar from '../avatar/role-avatar';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import { EditOutlined } from '@ant-design/icons';


const WikiSidebar = (wiki) => {
  const location = useLocation();
  const navigate = useNavigate();
  wiki = wiki.wiki;
  const { t } = useTranslation();
  console.log('wiki :>> ', wiki.image);

  return (
    <Sider className='wiki-sidebar'>
        <Flex align='center' vertical>
          <Image src={wiki.image}></Image>
          <div className='rating-container'>
            <b>{wiki.rating}</b>
            <Rate style={{ marginLeft: 10 }} disabled allowHalf value={wiki.rating} />
          </div>
          <h2>{wiki.title}</h2>
          <span className='wiki-description'>{wiki.description}</span>
          <Button size='small' icon={<EditOutlined />} iconPosition='start' onClick={() => navigate(location.pathname + "/edit")} className='wiki-description'>{t('wikis.edit-wiki-button')}</Button>
          <div className='user-container'>
            <RoleAvatar image={wiki.author.image} username={wiki.author.name} role='Author'/>
          </div>
        </Flex>
      </Sider>
  );
};

export default WikiSidebar;
