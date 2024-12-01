import React from "react";
import "./article-list.css";
import Article from "../article/article";
import { Grid, Flex, Row, Col } from "antd";
import { useTranslation } from "react-i18next";

const { useBreakpoint } = Grid;

const ArticleList = ({ articleList }) => {
  const screens = useBreakpoint();
  const { t } = useTranslation('wiki');
  return (
    <Flex className="article-list" vertical gap="small" align="center">
      <Row className="article-info" justify="space-around" align="center">
        <Col md={8} sm={9} xs={24} align="center">
          {t("table-title")}
        </Col>
        <Col md={5} sm={0} xs={24} align="center">
          {t("table-author")}
        </Col>
        <Col md={4} sm={5} xs={24} align="center">
          {t("table-date")}
        </Col>
        <Col md={7} sm={10} xs={24} align="center">
          {t("table-rating")}
        </Col>
      </Row>

      {articleList.map((article) => (
        <Article key={article.id} article={article} />
      ))}
    </Flex>
  );
};

export default ArticleList;
