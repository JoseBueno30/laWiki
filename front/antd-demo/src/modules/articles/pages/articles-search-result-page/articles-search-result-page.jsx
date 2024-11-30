import React, { useEffect, useState } from "react";
import "./articles-search-result-page.css";
import { Flex, Row, Col, Button } from "antd";
import { useSearchParams, useNavigate, useLocation, Link } from "react-router-dom";
import ArticleList from "../../components/article-list/article-list";
import axios from "axios";

const wiki_id = "672c8721ba3ae42bd5985361";
const searchLimit = 1;

const ArticlesSearchResultPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const paginationURL = location.state;
  const [searchParams, setSearchParams] = useSearchParams();
  const [currentPage, setCurrentPage] = useState(searchParams.get("page")?Number(searchParams.get("page")):1);
  
  const [loading, setLoading] = useState(true);
  
  const [filters, setFilters] = useState(null);
  const [response, setResponse] = useState(null);
  const [articles, setArticles] = useState([]);
  const [prevPageURL, setPrevPageURL] = useState(null);
  const [nextPageURL, setNextPageURL] = useState(null);

  const getNextArticlesSearchResultPage = async(url) =>{
    let newSearchParams = location.search;
    if(newSearchParams.includes("&page=")){
      newSearchParams = newSearchParams.replace(("&page="+currentPage), ("&page="+(currentPage+1)));
    }else{
      newSearchParams += "&page="+(currentPage+1);
    }
    setCurrentPage(currentPage+1);
    navigate(location.pathname + newSearchParams, {
      state: url ,
    });
  }

  const getPrevArticlesSearchResultPage = async(url) =>{
    let newSearchParams = location.search;
    if(newSearchParams.includes("&page=")){
      newSearchParams = newSearchParams.replace(("&page="+currentPage), ("&page="+(currentPage-1)));
    }else{
      newSearchParams += "&page="+(currentPage-1);
    }
    setCurrentPage(currentPage-1);
    navigate(location.pathname + newSearchParams, {
      state: url ,
    });
  }

  const formatFilters = (queryParams) => {
    delete queryParams.wiki_id;
    delete queryParams.name;
    delete queryParams.offset;
    delete queryParams.limit;

    let filterParams = new URLSearchParams(queryParams).toString().replaceAll("&", " | ").replaceAll("=", " : ");

    setFilters(filterParams);
  }


  const searchArticles = async () => {
    setLoading(true);
    try {
      
      var queryParams = {
        wiki_id: wiki_id,
        name: searchParams.get("name") || "",
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
      console.log(paginationURL);
      if(paginationURL!=null){
        HTTPResponse = await axios.get(
          "http://localhost:3000/v1" + paginationURL,
        );
      }else{
        HTTPResponse = await axios.get(
          "http://localhost:3000/v1/articles",
          { params: queryParams }
        );
      }
      
      setArticles(HTTPResponse.data.articles);
      setPrevPageURL(HTTPResponse.data.previous);
      setNextPageURL(HTTPResponse.data.next);
      setResponse(HTTPResponse.data);

      formatFilters(queryParams);

    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setLoading(true);
    searchArticles();
  }, [wiki_id, searchParams, paginationURL]);

  return (
    <>
      {loading || response==null ? (
        <p>CARGANDO</p>
      ) : (
        <Flex vertical align="center" style={{ minWidth: 400 }}>
          <h2 className="article-search-results-title">
            Search results for: {searchParams.get("name") || ""}
          </h2>
          <h3 className="article-search-results-info">
            Total: {response.total} | Filters: {filters}{/* MAKE A VARIABLE THAT HAS THE PROPER STRING WITH THE DESIRED FILTERS */}
          </h3>
          <ArticleList articleList={articles} />
          <Row
            align="middle"
            justify="space-around"
            style={{ width: "80%", marginTop: 20 }}
          >
            <Col>
                <Button type="primary" disabled={prevPageURL == null} onClick={() => getPrevArticlesSearchResultPage(prevPageURL)}>
                  Previous
                </Button>
            </Col>
            <Col>
              Page {Math.ceil(response.offset + 1 / response.limit)} of {Math.ceil(response.total / response.limit)}
            </Col>
            <Col>
              <Button type="primary" disabled={nextPageURL == null} onClick={() => getNextArticlesSearchResultPage(nextPageURL)}>
                Next
              </Button>
            </Col>
          </Row>
        </Flex>
      )}
    </>
  );
};

export default ArticlesSearchResultPage;
