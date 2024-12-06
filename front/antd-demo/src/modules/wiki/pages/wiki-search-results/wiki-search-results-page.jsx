import { Flex, Typography, Spin, Row, Col, Button } from "antd";
const { Title } = Typography;
import { useSearchParams, useLocation, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useState, useEffect, useContext } from "react";

import { SettingsContext } from "../../../../context/settings-context";
import WikiCardGrid from "../../components/wiki-card-grid/wiki-card-grid";
import WikiService from "../../service/wiki-service";
const { searchWikis } = WikiService();

const searchLimit = 6;

const WikiSearchResultsPage = () => {
  const { t } = useTranslation();
  const { locale } = useContext(SettingsContext);
  const [searchParams, setSearchParams] = useSearchParams();
  const location = useLocation();
  const navigate = useNavigate();

  const pagination_url = location.state;
  const [wikis, setWikis] = useState([]);
  const [prevPageURL, setPrevPageURL] = useState(null);
  const [nextPageURL, setNextPageURL] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [filters, setFilters] = useState(null);

  const [loading, setLoading] = useState(true);
  const [response, setResponse] = useState(null);

  const navigateToPage = (pagination_url, next_page) => {
    let newSearchParams = new URLSearchParams(location.search);
    newSearchParams.set("page", next_page);

    navigate(location.pathname + "?" + newSearchParams, {
      state: pagination_url,
    });
  };

  const updateState = (http_response) => {
    setResponse(http_response);
    setWikis(http_response.wikis);
    setPrevPageURL(http_response.prev);
    setNextPageURL(http_response.next);

    formatFilters(http_response.query_params);
  };

  const getWikiResults = async () => {
    try {
      const queryParams = retrieveSearchParams();
      // Actualiza la página y elimina el parámetro
      setCurrentPage(Number(queryParams["page"]));
      delete queryParams["page"];

      console.log("QUERY PARAMS", queryParams);
      const http_response = await searchWikis(queryParams);
      console.log("HTTP RESPONSE", http_response.wikis);
      updateState(http_response);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getWikiResultsByPaginationURL = async (url) => {
    try {
      const http_response = await getWikiResultsByPaginationURL(url);
      updateState(http_response);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const retrieveSearchParams = () => {
    const queryParams = {};
    queryParams["name"] = (searchParams.get("name") || "").replace("_", " ");
    queryParams["order"] = searchParams.get("order");
    if (searchParams.has("creation_date"))
      queryParams["creation_date"] = searchParams.get("creation_date");
    if (searchParams.has("author_name"))
      queryParams["author_name"] = searchParams.get("author_name");
    queryParams["offset"] = (currentPage - 1) * searchLimit;
    queryParams["limit"] = searchLimit;

    return queryParams;
  };

  const formatFilters = (queryParams) => {
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

  useEffect(() => {
    console.log("USE EFFECT");
    setLoading(true);
    if (pagination_url != null) {
      getWikiResultsByPaginationURL(pagination_url);
    } else {
      getWikiResults();
    }
  }, [searchParams, locale]);

  return (
    <Flex vertical style={{ width: "100%", paddingLeft:"50px" }}>
      {loading || response == null ? (
        <Spin size="large" style={{ paddingTop: "40vh" }} />
      ) : (
        <>
          <Title level={3}>
            {t("search.search-results", {
              query: (searchParams.get("name") || "").replace("_", " "),
            })}
          </Title>
          <Title level={4}>
            {t("search.search-description", {
              total: response.total,
              filters: filters,
            })}
          </Title>
          {wikis.length == 0 ? (
            <Title level={3}>{t("search.search-noresults")}</Title>
          ) : (
            <>
              <WikiCardGrid wikiList={wikis} />
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
                    onClick={() => navigateToPage(prevPageURL, currentPage - 1)}
                  >
                    {t("common.previous-page")}
                  </Button>
                </Col>
                <Col xs={24} sm={8} align="center">
                  Page {currentPage} of{" "}
                  {Math.ceil(response.total / response.limit)}
                </Col>
                <Col xs={24} sm={8} align="center">
                  <Button
                    type="primary"
                    disabled={nextPageURL == null}
                    onClick={() => navigateToPage(nextPageURL, currentPage + 1)}
                  >
                    {t("common.next-page")}
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

export default WikiSearchResultsPage;
