import React, { useEffect, useState, useContext } from "react";
import "./articles-search-result-page.css";
import { Flex, Row, Col, Button, Spin } from "antd";
import {
  useSearchParams,
  useNavigate,
  useLocation,
} from "react-router-dom";
import ArticleList from "../../components/article-list/article-list";
import { searchArticlesWithParams, searchArticlesWithPaginationURL } from "../../service/article_service";
import { useTranslation } from "react-i18next";
import { WikiContext } from "../../../../context/wiki-context";

const searchLimit = 3;

const ArticlesSearchResultPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const paginationURL = location.state;
  const [searchParams, setSearchParams] = useSearchParams();
  const [currentPage, setCurrentPage] = useState(searchParams.get("page") ? Number(searchParams.get("page")) : 1);

  const [loading, setLoading] = useState(true);

  const [filters, setFilters] = useState(null);
  const [response, setResponse] = useState(null);
  const [articles, setArticles] = useState([]);
  const [prevPageURL, setPrevPageURL] = useState(null);
  const [nextPageURL, setNextPageURL] = useState(null);

  const { t } = useTranslation('search');
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
      .replaceAll("_", " ");

    setFilters(filterParams);
  };

  const searchArticles = async () => {
    setLoading(true);
    try {

      var queryParams = {
        wiki_id: wiki.wiki_info.id,
        name: (searchParams.get("name") || "").replace("_", " "),
        tags: searchParams.getAll("tags"),
        offset: (currentPage - 1) * searchLimit,
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
      
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    console.log("USE EFFECT");
    setLoading(true);
    if(wiki.wiki_info!=null){
      searchArticles();
    }
  }, [wiki, searchParams]);

  return (
    <Flex gap="middle" vertical align="center" style={{ minWidth: 400 }}>
      {loading || response == null ? (
        <Spin size="large" style={{ paddingTop: "40vh" }} />
      ) : (
        <>
          <h2 className="article-search-results-title">
            {t("search-results", {query: (searchParams.get("name") || "").replace("_", " ")})}
          </h2>
          <h3 className="article-search-results-info">
            {t("search-description", {total: response.total, filters: filters})}
          </h3>
          {articles.length == 0 ? (
            <h2>{t("search-noresults")}</h2>
          ) : (
            <>
              <ArticleList articleList={articles} />
              <Row
                align="middle"
                justify="space-around"
                style={{ width: "80%", marginTop: 20 }}
              >
                <Col>
                  <Button
                    type="primary"
                    disabled={prevPageURL == null}
                    onClick={() => getArticlesSearchResultPage(prevPageURL, -1)}
                  >
                    {t("previous-page")}
                  </Button>
                </Col>
                <Col>
                  Page {currentPage} of{" "}
                  {Math.ceil(response.total / response.limit)}
                </Col>
                <Col>
                  <Button
                    type="primary"
                    disabled={nextPageURL == null}
                    onClick={() => getArticlesSearchResultPage(nextPageURL, 1)}
                  >
                    {t("next-page")}
                  </Button>
                </Col>
              </Row>
            </>
          )}
        </>
      )}
    </Flex>
  );
};

export default ArticlesSearchResultPage;
