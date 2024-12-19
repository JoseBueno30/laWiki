import React, { useEffect, useState, useContext } from "react";
import "./UserArticles.css";
import { Flex, Row, Col, Button, Spin } from "antd";
import {
    useSearchParams,
    useNavigate,
    useLocation,
} from "react-router-dom";
import ArticleList from "../../../articles/components/article-list/article-list";
import { useTranslation } from "react-i18next";
import { Typography } from "antd";
import ArticleService from "../../../articles/service/article-service";
const { searchArticlesByAuthor, searchArticlesWithPaginationURL } = ArticleService();

const { Title, Text } = Typography;

const UserArticles = ({
    author_name = "",
    author_id = "",
    order = "recent",
    active = false,
    search_limit = 6
}) => {
    const regexRemoveVersion = /\/v[0-9]+/g;
    const navigate = useNavigate();
    const location = useLocation();
    const paginationURL = location.state;
    const [searchParams, setSearchParams] = useSearchParams();
    const [currentPage, setCurrentPage] = useState(1);

    const [loading, setLoading] = useState(true);

    const [response, setResponse] = useState(null);
    const [articles, setArticles] = useState([]);
    const [prevPageURL, setPrevPageURL] = useState(null);
    const [nextPageURL, setNextPageURL] = useState(null);

    const { t } = useTranslation();

    const getArticlesSearchResultPage = async (url, increase) => {
        let newSearchParams = new URLSearchParams(location.search);

        newSearchParams.set("article_page", currentPage + increase);

        setCurrentPage(currentPage + increase);
        navigate(location.pathname + "?" + newSearchParams, {state: url});
    };

    const searchArticles = async () => {
        setLoading(true);
        try {

            var queryParams = {
                id: author_id,
                offset: ((searchParams.get("article_page") || 1) - 1) * search_limit,
                limit: search_limit,
                order: order
            };

            queryParams = Object.fromEntries(
                Object.entries(queryParams).filter(
                    ([_, value]) => value && value.length !== 0
                )
            );

            var HTTPResponse;
            if (paginationURL != null) {
                HTTPResponse = await searchArticlesWithPaginationURL(paginationURL.replace(regexRemoveVersion, ""));
            } else {
                HTTPResponse = await searchArticlesByAuthor(author_id, queryParams);
            }

            setArticles(HTTPResponse.articles);
            setPrevPageURL(HTTPResponse.previous?.replace(regexRemoveVersion, ""));
            setNextPageURL(HTTPResponse.next?.replace(regexRemoveVersion, ""));
            setResponse(HTTPResponse);

            if (searchParams.has("article_page")) setCurrentPage(Number(searchParams.get("article_page")))

        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        setLoading(true);
            searchArticles();
    }, [searchParams]);

    return (
        <Flex vertical align="center" style={{ width: "100%", marginBottom: 10 }}>
            {loading || response == null ? (
                <Spin size="large" style={{ paddingTop: "40vh" }} />
            ) : (
                <>
                    {!articles?.length ? (
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

export default UserArticles;
