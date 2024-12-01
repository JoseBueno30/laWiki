
import React from 'react';
import './wiki-main-page.css';
import WikiSidebar from '../../components/wiki-sidebar/wiki-sidebar';
import ArticleList from '../../../articles/components/article-list/article-list';
import { Col, Flex, Row } from 'antd';
import { useTranslation } from 'react-i18next';

const example = {
    title: 'Angular',
    description: 'Angular is a platform and framework for building single-page client applications using HTML and TypeScript.',
    rating: 4.6,
    image: 'https://upload.wikimedia.org/wikipedia/commons/c/cf/Angular_full_color_logo.svg',
    author:{
      name: 'John Doe',
      avatar: 'https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png'
    }
};



const WikiMainPage = () => {
  const { t } = useTranslation('wiki');
  return (
    <>
    <Flex className='wiki-page-wrapper'>
      <Row className='wiki-article-recommendation-wrapper'>
        <Col className='wiki-sidebar-container'>
          <WikiSidebar className="sidebar" {...example} />
        </Col>
        <Col className='wiki-content-wrapper'>
          <h2>{t('highest-rated-articles')}</h2>
          <ArticleList articleList={[example, example, example, example, example]} />
          <h2>{t('recent-articles')}s</h2>
          <ArticleList articleList={[example, example, example, example, example]} />
        </Col>
      </Row>
    </Flex>
    </>
  );
};

export default WikiMainPage;
