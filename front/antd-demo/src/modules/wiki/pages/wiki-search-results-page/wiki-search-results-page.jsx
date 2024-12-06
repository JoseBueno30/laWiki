import { Flex, Typography, Spin, Row, Col, Button } from "antd";
const { Title } = Typography;
import { useSearchParams, useLocation, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useState, useEffect, useContext } from "react";

import { SettingsContext } from "../../../../context/settings-context";
import WikiCardGrid from "../../components/wiki-card-grid/wiki-card-grid";
import WikiService from "../../service/wiki-service";
const { searchWikisWithParams, searchWikisWithPaginationURL } = WikiService();

const searchLimit = 6;

const WikiSearchResultsPage = () => {
  const { t } = useTranslation();
  const { locale } = useContext(SettingsContext);
  
  const [searchParams, setSearchParams] = useSearchParams();
  const location = useLocation();
  const navigate = useNavigate();
  const pagination_url = location.state;
  
  const [loading, setLoading] = useState(true);
  
  const [wikis, setWikis] = useState([]);
  const [prevPageURL, setPrevPageURL] = useState(null);
  const [nextPageURL, setNextPageURL] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [filters, setFilters] = useState(null);

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
    setPrevPageURL(http_response.previous);
    setNextPageURL(http_response.next);
  };

  const searchWikis = async () => {
    setLoading(true);
    try {

      const queryParams = retrieveSearchParams();

      var HTTPResponse;
      if (pagination_url != null) {
        HTTPResponse = await searchWikisWithPaginationURL(pagination_url);
      } else {
        HTTPResponse = await searchWikisWithParams(queryParams);
      }

      updateState(HTTPResponse);

      formatFilters(queryParams);

      if (searchParams.get("page")) setCurrentPage(Number(searchParams.get("page")))
      
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const retrieveSearchParams = () => {
    var queryParams = {
      name: (searchParams.get("name") || "").replaceAll("_", " "),
      offset: ((searchParams.get("page") || 1) - 1) * searchLimit,
      limit: searchLimit,
      order: searchParams.get("order") || "",
      creation_date: searchParams.get("creation_date") || "",
      author_name: searchParams.get("author_name") || "",
      lang: locale,
    };

    queryParams = Object.fromEntries(
      Object.entries(queryParams).filter(
        ([_, value]) => value && value.length !== 0
      )
    );

    return queryParams;
  };

  const formatFilters = (queryParams) => {
    delete queryParams.name;
    delete queryParams.offset;
    delete queryParams.limit;
    delete queryParams.lang;

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
    searchWikis();
  }, [searchParams, locale]);

  return (
    <Flex vertical align="center" style={{ width: "100%", marginBottom: 10 }}>
      {loading || response == null ? (
        <Spin size="large" style={{ paddingTop: "40vh" }} />
      ) : (
        <>
          <Title level={3}>
            {t("search.search-results", {
              query: (searchParams.get("name") || "").replaceAll("_", " "),
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
