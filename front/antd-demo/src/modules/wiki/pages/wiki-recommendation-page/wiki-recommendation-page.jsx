import React, { useEffect, useState } from "react";
import "./wiki-recommendation-page.css";
import "../../../../assets/css/pages.css";
import WikiCardGrid from "../../components/wiki-card-grid/wiki-card-grid";
import apiClient from "../../../../interceptor/interceptor";
import { Spin } from "antd";
import { useTranslation } from 'react-i18next';
import WikiService from "../../service/wiki-service";
const { getRatedWikis } = WikiService();

const WikiRecommendationPage = () => {
  const { t } = useTranslation();
  const [wikiList, setWikiList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHighestRatedWikis = async () => {
        const response = await getRatedWikis();
        setWikiList(response.wikis);
        setLoading(false);
    };

    fetchHighestRatedWikis();
  }, []);

  return (
    <>
      <div className="page-wrapper">
        <div className="md-flex">
          <h1>{t('wikis.highest-rated-wikis')}</h1>
        </div>
        {loading ? (
          <Spin></Spin>
        ) : (
          <WikiCardGrid wikiList={wikiList} />
        )}
      </div>
    </>
  );
};

export default WikiRecommendationPage;
