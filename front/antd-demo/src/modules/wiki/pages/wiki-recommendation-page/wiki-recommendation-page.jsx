import React, { useEffect, useState, useContext } from "react";
import "./wiki-recommendation-page.css";
import "../../../../assets/css/pages.css";
import WikiCardGrid from "../../components/wiki-card-grid/wiki-card-grid";
import apiClient from "../../../../interceptor/interceptor";
import { Flex, Spin } from "antd";
import { useTranslation } from 'react-i18next';
import WikiService from "../../service/wiki-service";
const { getRatedWikis } = WikiService();
import { SettingsContext } from "../../../../context/settings-context";

const WikiRecommendationPage = () => {
  const { locale } = useContext(SettingsContext);
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
  }, [locale]);

  return (
    <>
      <div className="page-wrapper">
        <div className="md-flex">
          <h1>{t('wikis.highest-rated-wikis')}</h1>
        </div>
        {loading ? (
          <Flex vertical align="center" style={{ width: "100%", marginBottom: 10 }}>
            <Spin></Spin>
          </Flex>
        ) : (
          <WikiCardGrid wikiList={wikiList} />
        )}
      </div>
    </>
  );
};

export default WikiRecommendationPage;
