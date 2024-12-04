
import React from 'react';
import './wiki-main-page.css';
import WikiSidebar from '../../components/wiki-sidebar/wiki-sidebar';
import ArticleList from '../../../articles/components/article-list/article-list';
import { Col, Flex, Row, Spin } from 'antd';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useContext } from 'react';
import WikiService from "../../service/wiki-service";
import { WikiContext } from '../../../../context/wiki-context';
import { searchArticlesWithParams } from '../../../articles/service/article_service';

const WikiMainPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { wiki } = useContext(WikiContext);
  const [ratedArticles, setRatedArticles] = useState([]);
  const [recentArticles, setRecentArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const searchLimit = 5;

  useEffect(() => {
    const fetchWikiArticles = async () => {
        var queryParamsPopular = {
          wiki_id: wiki.wiki_info.id,
          limit: searchLimit,
          order: "popular",
          lan: "",
        };

        queryParamsPopular = Object.fromEntries(
          Object.entries(queryParamsPopular).filter(
            ([_, value]) => value && value.length !== 0
          )
        );

        var queryParamsRecent = {
          wiki_id: wiki.wiki_info.id,
          limit: searchLimit,
          order: "recent",
          lan: "",
        };

        queryParamsRecent = Object.fromEntries(
          Object.entries(queryParamsRecent).filter(
            ([_, value]) => value && value.length !== 0
          )
        );
        const ratedArticles = await searchArticlesWithParams(queryParamsPopular);
        const recentArticles = await searchArticlesWithParams(queryParamsRecent);
        setRatedArticles(ratedArticles);
        setRecentArticles(recentArticles);
        setLoading(false);
    };

    fetchWikiArticles();
  }, [wiki]);

  return (
    <>
      {wiki && wiki.wiki_info ? (
        <Flex className='wiki-page-wrapper'>
        <Row className='wiki-article-recommendation-wrapper'>
          <Col className='wiki-sidebar-container'>
            <WikiSidebar className="sidebar" wiki={wiki.wiki_info} />
          </Col>
          <Col className='wiki-content-wrapper'>
            <h2>{t('article.highest-rated-articles')}</h2>
            {ratedArticles && ratedArticles.articles ? (
            <ArticleList articleList={ratedArticles.articles ?? []} />)
            : (
              <Spin></Spin>
            )}
            <h2>{t('article.recent-articles')}</h2>
            {recentArticles && recentArticles.articles ? (
            <ArticleList articleList={recentArticles.articles ?? []} />)
            : (
              <Spin></Spin>
            )}
          </Col>
        </Row>
      </Flex>
      ) : (
        <div className='spinner'>
          <Spin></Spin>
        </div>
      )}
      
    </>
  );
};

export default WikiMainPage;
