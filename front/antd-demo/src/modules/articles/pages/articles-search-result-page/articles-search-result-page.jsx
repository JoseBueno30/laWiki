import React, { useEffect, useState, useContext } from "react";
import "./articles-search-result-page.css";
import { Flex, Row, Col, Button, Spin, Space } from "antd";
import {
  useSearchParams,
  useNavigate,
  useLocation,
} from "react-router-dom";
import ArticleList from "../../components/article-list/article-list";
import {  } from "../../service/article_service";
const { searchArticlesWithParams, searchArticlesWithPaginationURL } = ArticleService();
import { useTranslation } from "react-i18next";
import { WikiContext } from "../../../../context/wiki-context";
import { Typography } from "antd";
import ArticleService from "../../service/article-service";

const { Title, Text } = Typography;

const searchLimit = 3;

const ArticlesSearchResultPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const paginationURL = location.state;
  const [searchParams, setSearchParams] = useSearchParams();
  const [currentPage, setCurrentPage] = useState(1);

  const [loading, setLoading] = useState(true);

  const [filters, setFilters] = useState(null);
  const [response, setResponse] = useState(null);
  const [articles, setArticles] = useState([]);
  const [prevPageURL, setPrevPageURL] = useState(null);
  const [nextPageURL, setNextPageURL] = useState(null);

  const { t } = useTranslation();
  const { wiki } = useContext(WikiContext);

  const getArticlesSearchResultPage = async (url, increase) => {
    let newSearchParams = new URLSearchParams(location.search);

    newSearchParams.set("page", currentPage + increase);

    setCurrentPage(currentPage + increase);
    navigate(location.pathname + "?" + newSearchParams, {state: url});
  };

  const formatFilters = (queryParams) => {
    delete queryParams.wiki_id;
    delete queryParams.name;
    delete queryParams.offset;
    delete queryParams.limit;

    let filterParams = new URLSearchParams(queryParams)
      .toString()
      .replaceAll("&", " | ")
      .replaceAll("=", " : ")
      .replaceAll("_", " ")
      .replaceAll("%2F", "/");

    setFilters(filterParams);
  };

  const searchArticles = async () => {
    setLoading(true);
    try {

      var queryParams = {
        wiki_id: wiki.wiki_info.id,
        name: (searchParams.get("name") || "").replaceAll("_", " "),
        tags: searchParams.getAll("tags"),
        offset: ((searchParams.get("page") || 1) - 1) * searchLimit,
        limit: searchLimit,
        order: searchParams.get("order") || "",
        creation_date: searchParams.get("creation_date") || "",
        author_name: searchParams.get("author_name") || "",
        editor_name: searchParams.get("editor_name") || "",
        lan: "",
      };

      queryParams = Object.fromEntries(
        Object.entries(queryParams).filter(
          ([_, value]) => value && value.length !== 0
        )
      );

      var HTTPResponse;
      if (paginationURL != null) {
        HTTPResponse = await searchArticlesWithPaginationURL(paginationURL);
      } else {
        HTTPResponse = await searchArticlesWithParams(queryParams);
      }

      setArticles(HTTPResponse.articles);
      setPrevPageURL(HTTPResponse.previous);
      setNextPageURL(HTTPResponse.next);
      setResponse(HTTPResponse);

      formatFilters(queryParams);
      if (searchParams.get("page")) setCurrentPage(Number(searchParams.get("page")))
      
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setLoading(true);
    if(wiki.wiki_info!=null){
      searchArticles();
    }
  }, [wiki, searchParams]);

  return (
    <Flex vertical align="center" style={{ width: "100%", marginBottom: 10 }}>
      {loading || response == null ? (
        <Spin size="large" style={{ paddingTop: "40vh" }} />
      ) : (
        <>
          <Title level={3} className="article-search-results-title">
            {t("search.search-results", {query: (searchParams.get("edit.name") || "").replaceAll("_", " ")})}
          </Title>
          <Title level={4} className="article-search-results-info">
            {t("search.search-description", {total: response.total, filters: filters})}
          </Title>
          {articles.length == 0 ? (
            <Title level={3}>{t("search.search-noresults")}</Title>
          ) : (
            <Flex vertical align="center" style={{width:"85%"}}>
              <ArticleList articleList={articles}/>
              <Row
                align="middle"
                justify="space-around"
                style={{ width: "80%", marginTop: 20 }}
                gutter={[16, 16]}
              >
                <Col xs={24} sm={8} align="center">
                  <Button
                    type="primary"
                    disabled={prevPageURL == null}
                    onClick={() => getArticlesSearchResultPage(prevPageURL, -1)}
                  >
                    {t("common.previous-page")}
                  </Button>
                </Col>
                <Col xs={24} sm={8} align="center">
                  {t("common.pagination", {page:currentPage, total: Math.ceil(response.total / response.limit)})}
                </Col>
                <Col xs={24} sm={8} align="center">
                  <Button
                    type="primary"
                    disabled={nextPageURL == null}
                    onClick={() => getArticlesSearchResultPage(nextPageURL, 1)}
                  >
                    {t("common.next-page")}
                  </Button>
                </Col>
              </Row>
            </Flex>
          )}
        </>
      )}
    </Flex>
  );
};

export default ArticlesSearchResultPage;
