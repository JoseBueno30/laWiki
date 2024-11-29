import React, { useEffect, useState } from "react";
import "./articles-search-result-page.css";
import { Flex, Row, Col, Button } from "antd";
import { useSearchParams, useNavigate, useLocation, Link } from "react-router-dom";
import ArticleList from "../../components/article-list/article-list";
import axios from "axios";

const wiki_id = "672c8721ba3ae42bd5985361";

const ArticlesSearchResultPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const basePath = useLocation().pathname;
  const [loading, setLoading] = useState(true);
  const [articles, setArticles] = useState([]);
  const [prevPageURL, setPrevPageURL] = useState(null);
  const [nextPageURL, setNextPageURL] = useState(null);
  const [response, setResponse] = useState(null);
  const [filters, setFilters] = useState(null);

  // TODO: In order to search in a given wiki, should the gateway provide an endpoint to search having only the wiki name? or should the front handle this

  const searchArticles = async () => {
    setLoading(true);
    try {
      var params = {
        wiki_id: wiki_id,
        name: searchParams.get("name") || "",
        tags: searchParams.getAll("tags"),
        offset: searchParams.get("offset") || 0,
        limit: 1,
        order: searchParams.get("order") || "",
        creation_date: searchParams.get("creation_date") || "",
        author_name: searchParams.get("author_name") || "",
        editor_name: searchParams.get("editor_name") || "",
        lan: "es",
      };

      params = Object.fromEntries(
        Object.entries(params).filter(
          ([_, value]) => value && value.length !== 0
        )
      );

      
      
      const HTTPresponse = await axios.get(
        "http://localhost:3000/v1/articles",
        { params: params }
      );
      
      setArticles(HTTPresponse.data.articles);
      setPrevPageURL(HTTPresponse.data.previous);
      setNextPageURL(HTTPresponse.data.next);
      setResponse(HTTPresponse.data);
      
      delete params.wiki_id;
      delete params.name;
      delete params.offset;
      delete params.limit;
      
      setFilters(params);

      console.log(params)
      console.log(filters)
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setLoading(true);
    searchArticles();
  }, [wiki_id, searchParams]);

  return (
    <>
      {loading ? (
        <p>CARGANDO</p>
      ) : (
        <Flex vertical align="center" style={{ minWidth: 400 }}>
          <h2 className="article-search-results-title">
            Search results for: {searchParams.get("name") || ""}
          </h2>
          <h3 className="article-search-results-info">
            Total: {response.total} | Filters: {new URLSearchParams(filters).toString().replaceAll("&", " | ").replaceAll("=", " : ")}{/* MAKE A VARIABLE THAT HAS THE PROPER STRING WITH THE DESIRED FILTERS */}
          </h3>
          <ArticleList articleList={articles} />
          <Row
            align="middle"
            justify="space-around"
            style={{ width: "80%", marginTop: 20 }}
          >
            <Col>
              <Link to={basePath + "?" + new URLSearchParams(prevPageURL).toString()}>{/* SHOULD PAGINATION RELOAD THE PAGE OR JUST MAKE NEW PETITIONS? */}
                <Button type="primary" disabled={prevPageURL == null}>
                  Previous
                </Button>
              </Link>
            </Col>
            <Col>
              Page {Math.ceil(response.offset + 1 / response.limit)} of {Math.ceil(response.total / response.limit)}
            </Col>
            <Col>
            <Link to={basePath + "?" + new URLSearchParams(nextPageURL).toString()}>
              {console.log(new URLSearchParams(nextPageURL.rem))}
              <Button type="primary" disabled={nextPageURL == null}>
                Next
              </Button>
            </Link>
            </Col>
          </Row>
        </Flex>
      )}
    </>
  );
};

export default ArticlesSearchResultPage;
